"""Test script for ML-based evaluation service."""

import asyncio
import sys
from pathlib import Path

# Add apps/api to path
api_dir = Path(__file__).parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from app.services.evaluation_service import get_evaluation_service


def test_ml_evaluation():
    """Test the ML evaluation service with sample answers."""
    
    print("=" * 60)
    print("ML-BASED EVALUATION TEST")
    print("=" * 60)
    print()
    
    # Sample answers
    student_answer = "Photosynthesis happens in leaves using sunlight and chlorophyll."
    reference_answer = "Photosynthesis is the process by which green plants use sunlight to synthesize food from carbon dioxide and water."
    
    print("Student Answer:")
    print(f"  {student_answer}")
    print()
    print("Reference Answer:")
    print(f"  {reference_answer}")
    print()
    print("-" * 60)
    print("Running ML Evaluation...")
    print("-" * 60)
    print()
    
    # Get evaluation service
    try:
        evaluation_service = get_evaluation_service()
        print(f"✅ Evaluation service initialized")
        print(f"✅ Model loaded: {evaluation_service.model is not None}")
        print()
    except Exception as e:
        print(f"❌ Error initializing evaluation service: {e}")
        return
    
    # Run evaluation
    try:
        result = evaluation_service.evaluate_answer(student_answer, reference_answer)
        
        print("=" * 60)
        print("EVALUATION RESULTS")
        print("=" * 60)
        print()
        print(f"Similarity:  {result['similarity']:.4f} ({result['similarity']*100:.2f}%)")
        print(f"Score:       {result['score']:.2f} / 10.0")
        print(f"Confidence:  {result['confidence']:.4f} ({result['confidence']*100:.2f}%)")
        print(f"Method:      {result['method']}")
        print()
        
        # Validation
        print("=" * 60)
        print("VALIDATION")
        print("=" * 60)
        print()
        
        score_valid = 0 <= result['score'] <= 10
        confidence_valid = 0 < result['confidence'] <= 1
        similarity_valid = 0 <= result['similarity'] <= 1
        
        print(f"Score in range [0, 10]:     {'✅ PASS' if score_valid else '❌ FAIL'} (value: {result['score']:.2f})")
        print(f"Confidence > 0:             {'✅ PASS' if confidence_valid else '❌ FAIL'} (value: {result['confidence']:.4f})")
        print(f"Similarity in range [0, 1]: {'✅ PASS' if similarity_valid else '❌ FAIL'} (value: {result['similarity']:.4f})")
        print()
        
        if score_valid and confidence_valid and similarity_valid:
            print("✅ ALL VALIDATIONS PASSED")
        else:
            print("❌ SOME VALIDATIONS FAILED")
        
        print()
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error during evaluation: {e}")
        import traceback
        traceback.print_exc()
        return


if __name__ == "__main__":
    test_ml_evaluation()

