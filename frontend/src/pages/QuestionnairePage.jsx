import React, { useState, useEffect, useCallback } from 'react';
import { ArrowLeft, ArrowRight, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react';
import ProgressBar from '../components/ProgressBar';
import QuestionCard from '../components/QuestionCard';
import ReportView from './ReportView';
import { getQuestions, submitAssessment } from '../services/api';

export default function QuestionnairePage({ onBackToHome }) {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [fetchError, setFetchError] = useState(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState(null);
  const [result, setResult] = useState(null);

  useEffect(() => {
    const fetchQuestionsData = async () => {
      try {
        setLoading(true);
        const data = await getQuestions();
        setQuestions(data.questions);
        setFetchError(null);
      } catch (err) {
        console.error('Error fetching questions:', err);
        setFetchError('Unable to load assessment questions. Please ensure the backend server is running.');
      } finally {
        setLoading(false);
      }
    };

    fetchQuestionsData();
  }, []);

  const currentQuestion = questions[currentIndex];
  const totalQuestions = questions.length;
  const currentAnswer = currentQuestion ? answers[currentQuestion.id] : undefined;
  const hasAnsweredCurrent = currentAnswer !== undefined;

  const handleSelectOption = useCallback((value) => {
    if (!currentQuestion) return;
    setAnswers((prev) => ({
      ...prev,
      [currentQuestion.id]: value,
    }));
  }, [currentQuestion]);

  const handleSubmit = useCallback(async () => {
    const missing = questions.filter((q) => answers[q.id] === undefined);
    if (missing.length > 0) {
      setSubmitError(`Please answer all questions before completing. Missing: Question ${missing[0].id}`);
      return;
    }

    try {
      setIsSubmitting(true);
      setSubmitError(null);
      const res = await submitAssessment(answers);
      setResult(res);
    } catch (err) {
      console.error('Submission failed:', err);
      const errorMessage = err.response?.data?.detail
        ? (typeof err.response.data.detail === 'string' ? err.response.data.detail : 'Invalid input received by assessment service.')
        : 'Failed to process responses. Please check connection.';
      setSubmitError(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  }, [answers, questions]);

  const handleNext = useCallback(async () => {
    if (!hasAnsweredCurrent) return;

    if (currentIndex < totalQuestions - 1) {
      setCurrentIndex((prev) => prev + 1);
    } else {
      await handleSubmit();
    }
  }, [currentIndex, hasAnsweredCurrent, totalQuestions, handleSubmit]);

  const handleBack = () => {
    if (currentIndex > 0) {
      setCurrentIndex((prev) => prev - 1);
    } else if (onBackToHome) {
      onBackToHome();
    }
  };

  const handleRetake = () => {
    setAnswers({});
    setCurrentIndex(0);
    setResult(null);
    setSubmitError(null);
  };

  // Keyboard navigation support: 1-5 to select, Enter to advance
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (result || loading || isSubmitting) return;

      const num = parseInt(e.key, 10);
      if (num >= 1 && num <= 5) {
        handleSelectOption(num);
      } else if (e.key === 'Enter' && hasAnsweredCurrent) {
        handleNext();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [result, loading, isSubmitting, handleSelectOption, handleNext, hasAnsweredCurrent]);

  // If result is ready, display Results Screen
  if (result) {
    return (
      <ReportView
        result={result}
        onRetake={handleRetake}
        onHome={onBackToHome}
      />
    );
  }

  // Loading state
  if (loading) {
    return (
      <div className="max-w-xl mx-auto py-20 text-center space-y-4">
        <Loader2 className="w-8 h-8 text-sage-600 animate-spin mx-auto" />
        <p className="text-sm font-medium text-sage-800">
          Preparing your wellness assessment...
        </p>
      </div>
    );
  }

  // Error state
  if (fetchError) {
    return (
      <div className="max-w-xl mx-auto py-16 space-y-5 text-center">
        <div className="p-6 rounded-2xl bg-rose-50 border border-rose-200 text-rose-800 space-y-2 text-sm">
          <AlertCircle className="w-6 h-6 text-rose-600 mx-auto" />
          <strong className="block font-semibold">Connection Issue</strong>
          <p className="text-xs text-rose-700">{fetchError}</p>
        </div>
        <button
          type="button"
          onClick={onBackToHome}
          className="px-5 py-2.5 rounded-xl bg-sage-700 hover:bg-sage-800 text-white text-xs font-medium transition-colors cursor-pointer"
        >
          Return to Welcome
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto space-y-8 py-2 sm:py-4">
      {/* Progress Bar */}
      <ProgressBar
        current={currentIndex + 1}
        total={totalQuestions}
      />

      {/* Main Question Focus */}
      <QuestionCard
        question={currentQuestion}
        selectedValue={currentAnswer}
        onSelect={handleSelectOption}
      />

      {/* Error Alert */}
      {submitError && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-center space-x-2.5">
          <AlertCircle className="w-4 h-4 text-rose-600 flex-shrink-0" />
          <span>{submitError}</span>
        </div>
      )}

      {/* Navigation Controls */}
      <div className="flex items-center justify-between pt-2">
        <button
          type="button"
          onClick={handleBack}
          disabled={isSubmitting}
          className="inline-flex items-center space-x-1.5 px-4 py-2.5 rounded-xl border border-parchment-300 bg-white hover:bg-parchment-50 text-sage-800 text-sm font-medium transition-colors cursor-pointer"
        >
          <ArrowLeft className="w-4 h-4 text-sage-600" />
          <span>{currentIndex === 0 ? 'Exit to Welcome' : 'Back'}</span>
        </button>

        <span className="text-xs text-[#7E8B85] hidden sm:inline">
          {!hasAnsweredCurrent ? 'Select an answer to proceed' : 'Ready to continue (or press Enter)'}
        </span>

        <button
          type="button"
          onClick={handleNext}
          disabled={!hasAnsweredCurrent || isSubmitting}
          className={`inline-flex items-center space-x-2 px-6 py-2.5 rounded-xl text-sm font-medium transition-all shadow-sm ${
            !hasAnsweredCurrent || isSubmitting
              ? 'bg-parchment-300 text-parchment-900/40 cursor-not-allowed shadow-none'
              : 'bg-sage-700 hover:bg-sage-800 text-white cursor-pointer'
          }`}
        >
          {isSubmitting ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Analyzing responses...</span>
            </>
          ) : currentIndex === totalQuestions - 1 ? (
            <>
              <span>View Results</span>
              <CheckCircle2 className="w-4 h-4" />
            </>
          ) : (
            <>
              <span>Next</span>
              <ArrowRight className="w-4 h-4" />
            </>
          )}
        </button>
      </div>

      {/* Reassuring footer note */}
      <p className="text-center text-[11px] text-[#7E8B85]">
        All responses are anonymous and processed in-session for self-reflection.
      </p>
    </div>
  );
}
