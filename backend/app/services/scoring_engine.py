from typing import Dict, Any, Tuple

class MetricNormalizer:
    @staticmethod
    def normalize_latency(p95_latency: float, target_latency: float, rps: float) -> float:
        if rps <= 0:
            return 100.0 
        if target_latency <= 0:
            target_latency = 1.0 
        if p95_latency <= target_latency:
            return 100.0
        penalty = ((p95_latency - target_latency) / target_latency) * 50.0
        return max(0.0, 100.0 - penalty)
    @staticmethod
    def normalize_cost(actual_cost: float, budget: float) -> float:
    
        if budget <= 0:
            return 100.0 if actual_cost == 0 else 0.0   
        if actual_cost == 0:
            return 100.0    
        if actual_cost <= budget:
            return 100.0    
        penalty = ((actual_cost - budget) / budget) * 100.0
        return max(0.0, 100.0 - penalty)

    @staticmethod
    def normalize_efficiency(cpu_avg: float, capacity: float, rps: float) -> float:
        target_mid = 70.0
        if capacity <= 0:
            if rps > 0:
                cpu_val = 100.0
            else:
                return 100.0
        else:
            cpu_val = max(0.0, min(100.0, cpu_avg)) 
        distance = abs(cpu_val - target_mid)
        score = 100.0 - (distance * 1.5)
        return max(0.0, score)

    @staticmethod
    def normalize_reliability(dropped_requests: int, queue_ms: float) -> float:
        if dropped_requests > 0:
            return 0.0  
        if queue_ms > 1000.0:
            return 50.0
        return 100.0
class DecisionScorer:
       @staticmethod
    def get_grade(score: float, dropped_requests: int = 0) -> str:
        if dropped_requests > 0:
            if score >= 60.0:
                return "D"
            return "F"
            
        if score >= 90.0:
            return "A"
        elif score >= 80.0:
            return "B"
        elif score >= 70.0:
            return "C"
        elif score >= 60.0:
            return "D"
        else:
            return "F"

    @classmethod
    def calculate_score(
        cls, 
        raw_metrics: Dict[str, float], 
        weights: Dict[str, float], 
        constraints: Dict[str, float]
    ) -> Dict[str, Any]:

        dropped_requests = int(raw_metrics.get("dropped_requests", 0))
        score_L = MetricNormalizer.normalize_latency(
            p95_latency=raw_metrics.get("p95_latency", 0.0),
            target_latency=constraints.get("target_latency", 100.0),
            rps=raw_metrics.get("rps", 0.0)
        )
        
        score_C = MetricNormalizer.normalize_cost(
            actual_cost=raw_metrics.get("actual_cost", 0.0),
            budget=constraints.get("budget", 0.0)
        )
        
        score_E = MetricNormalizer.normalize_efficiency(
            cpu_avg=raw_metrics.get("cpu_avg", 0.0),
            capacity=raw_metrics.get("capacity", 1.0),
            rps=raw_metrics.get("rps", 0.0)
        )
        
        score_R = MetricNormalizer.normalize_reliability(
            dropped_requests=dropped_requests,
            queue_ms=raw_metrics.get("queue_ms", 0.0)
        )
     
        w_L = weights.get("wL", 0.25)
        w_C = weights.get("wC", 0.25)
        w_E = weights.get("wE", 0.25)
        w_R = weights.get("wR", 0.25)
       
        total_weight = w_L + w_C + w_E + w_R
        if total_weight > 0:
            w_L /= total_weight
            w_C /= total_weight
            w_E /= total_weight
            w_R /= total_weight
        final_score = (w_L * score_L) + (w_C * score_C) + (w_E * score_E) + (w_R * score_R)
        
       
        if dropped_requests > 0:
            final_score *= 0.4
            
        final_score = round(final_score, 1)
        return {
            "score": final_score,
            "grade": cls.get_grade(final_score, dropped_requests),
            "breakdown": {
                "latency": round(score_L, 1),
                "cost": round(score_C, 1),
                "efficiency": round(score_E, 1),
                "reliability": round(score_R, 1)
            }
        }
