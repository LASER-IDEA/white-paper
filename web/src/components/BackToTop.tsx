import React, { useState, useEffect, useRef } from 'react';

interface BackToTopProps {
  scrollContainerRef?: React.RefObject<HTMLElement | null>;
}

const BackToTop: React.FC<BackToTopProps> = ({ scrollContainerRef }) => {
  const [isVisible, setIsVisible] = useState(false);
  const [progress, setProgress] = useState(0);
  const rafRef = useRef<number | null>(null);

  useEffect(() => {
    const handleScroll = () => {
      if (rafRef.current) return;

      rafRef.current = requestAnimationFrame(() => {
        let scrollTop = 0;
        let scrollHeight = 0;
        let clientHeight = 0;

        if (scrollContainerRef?.current) {
          scrollTop = scrollContainerRef.current.scrollTop;
          scrollHeight = scrollContainerRef.current.scrollHeight;
          clientHeight = scrollContainerRef.current.clientHeight;
        } else {
          scrollTop = window.scrollY;
          scrollHeight = document.documentElement.scrollHeight;
          clientHeight = document.documentElement.clientHeight;
        }

        const winHeight = scrollHeight - clientHeight;
        const scrolled = winHeight > 0 ? (scrollTop / winHeight) * 100 : 0;

        setIsVisible(scrollTop > 300);
        setProgress(Math.min(100, Math.max(0, scrolled)));
        rafRef.current = null;
      });
    };

    // Determine target (Window or HTMLElement)
    const target = scrollContainerRef?.current || window;

    // Add event listener
    target.addEventListener('scroll', handleScroll as EventListener);

    // Check initial position
    handleScroll();

    return () => {
      target.removeEventListener('scroll', handleScroll as EventListener);
      if (rafRef.current) {
        cancelAnimationFrame(rafRef.current);
      }
    };
  }, [scrollContainerRef]);

  const scrollToTop = () => {
    if (scrollContainerRef?.current) {
      scrollContainerRef.current.scrollTo({
        top: 0,
        behavior: 'smooth',
      });
    } else {
      window.scrollTo({
        top: 0,
        behavior: 'smooth',
      });
    }
  };

  // Circle properties
  const radius = 20;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (progress / 100) * circumference;

  return (
    <button
      type="button"
      onClick={scrollToTop}
      className={`fixed bottom-8 right-8 z-50 w-12 h-12 flex items-center justify-center rounded-full bg-[#002FA7] text-white shadow-lg transition-all duration-300 hover:bg-[#001F7A] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#002FA7] print:hidden no-print group ${
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10 pointer-events-none'
      }`}
      aria-label={`返回顶部 (当前阅读进度 ${Math.round(progress)}%)`}
    >
      {/* Progress Ring */}
      <svg className="absolute inset-0 w-full h-full -rotate-90 pointer-events-none p-1" viewBox="0 0 48 48">
        <circle
          cx="24" cy="24" r={radius}
          fill="none"
          stroke="rgba(255,255,255,0.2)"
          strokeWidth="3"
        />
        <circle
          cx="24" cy="24" r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth="3"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          className="transition-all duration-100 ease-out text-white opacity-90"
        />
      </svg>

      <svg className="w-5 h-5 relative z-10 transition-transform group-hover:-translate-y-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 10l7-7m0 0l7 7m-7-7v18" />
      </svg>
    </button>
  );
};

export default BackToTop;
