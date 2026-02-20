// OpenClaw Book - Custom JavaScript
// Automatically classify blockquotes based on emoji content

(function() {
    'use strict';

    // Wait for DOM to be fully loaded
    function initCalloutBoxes() {
        // Find all blockquotes in the content
        const blockquotes = document.querySelectorAll('.content blockquote');
        
        blockquotes.forEach(function(blockquote) {
            const text = blockquote.textContent || blockquote.innerText;
            
            // Check for specific emoji patterns
            if (text.includes('💡')) {
                blockquote.classList.add('callout-tip');
            } else if (text.includes('🔧')) {
                blockquote.classList.add('callout-error');
            } else if (text.includes('📚')) {
                blockquote.classList.add('callout-learn');
            }
            // You can add more emoji patterns here as needed
            // else if (text.includes('⚠️')) {
            //     blockquote.classList.add('callout-warning');
            // }
        });
    }

    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCalloutBoxes);
    } else {
        // DOM is already loaded
        initCalloutBoxes();
    }

    // Also run when navigating between pages in mdBook
    // mdBook uses history API for navigation
    window.addEventListener('popstate', function() {
        setTimeout(initCalloutBoxes, 100);
    });

    // Handle mdBook's internal navigation
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a');
        if (link && link.href && link.href.indexOf(window.location.origin) === 0) {
            // Internal link clicked, re-run after a short delay
            setTimeout(initCalloutBoxes, 100);
        }
    });

})();
