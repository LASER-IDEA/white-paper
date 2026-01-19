import React, { useState, useEffect } from 'react';

interface BackToTopProps {
  scrollContainerRef?: React.RefObject<HTMLElement | null>;
}

const BackToTop: React.FC<BackToTopProps> = ({ scrollContainerRef }) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      let scrollTop = 0;
      if (scrollContainerRef?.current) {
        scrollTop = scrollContainerRef.current.scrollTop;
      } else {
        scrollTop = window.scrollY;
      }
      setIsVisible(scrollTop > 300);
    };

    // Determine target (Window or HTMLElement)
    const target = scrollContainerRef?.current || window;

    // Add event listener
    // Note: TypeScript might infer strict types, casting to EventListener helps unify
    target.addEventListener('scroll', handleScroll as EventListener);

    // Check initial position
    handleScroll();

    return () => {
      target.removeEventListener('scroll', handleScroll as EventListener);
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

  return (
    <button
      type="button"
      onClick={scrollToTop}
      className={`fixed bottom-8 right-8 z-50 p-3 rounded-full bg-[#002FA7] text-white shadow-lg transition-all duration-300 hover:bg-[#001F7A] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#002FA7] print:hidden no-print ${
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10 pointer-events-none'
      }`}
      aria-label="返回顶部"
    >
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 10l7-7m0 0l7 7m-7-7v18" />
      </svg>
    </button>
  );
};

export default BackToTop;
