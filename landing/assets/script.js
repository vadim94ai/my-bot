document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });

        // Close mobile menu when clicking a link
        const mobileLinks = mobileMenu.querySelectorAll('a');
        mobileLinks.forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.add('hidden');
            });
        });
    }

    // Sticky navbar
    const navbar = document.getElementById('navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 10) {
                navbar.classList.add('shadow-md');
            } else {
                navbar.classList.remove('shadow-md');
            }
        });
    }

    // FAQ Accordion
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const button = item.querySelector('.faq-button');
        const content = item.querySelector('.faq-content');
        const icon = item.querySelector('svg');

        if (button && content) {
            button.addEventListener('click', () => {
                const isExpanded = button.getAttribute('aria-expanded') === 'true';
                
                // Close all others
                faqItems.forEach(otherItem => {
                    if (otherItem !== item) {
                        const otherButton = otherItem.querySelector('.faq-button');
                        const otherContent = otherItem.querySelector('.faq-content');
                        const otherIcon = otherItem.querySelector('svg');
                        
                        otherButton.setAttribute('aria-expanded', 'false');
                        otherContent.style.maxHeight = null;
                        otherContent.classList.remove('opacity-100');
                        otherContent.classList.add('opacity-0');
                        if(otherIcon) otherIcon.classList.remove('rotate-180');
                    }
                });

                // Toggle current
                button.setAttribute('aria-expanded', !isExpanded);
                if (!isExpanded) {
                    content.style.maxHeight = content.scrollHeight + "px";
                    content.classList.remove('opacity-0');
                    content.classList.add('opacity-100');
                    if(icon) icon.classList.add('rotate-180');
                } else {
                    content.style.maxHeight = null;
                    content.classList.remove('opacity-100');
                    content.classList.add('opacity-0');
                    if(icon) icon.classList.remove('rotate-180');
                }
            });
        }
    });

    // Scroll reveal animation
    const reveals = document.querySelectorAll('.reveal');
    const revealOptions = {
        threshold: 0.15,
        rootMargin: "0px 0px -50px 0px"
    };
    
    const revealObserver = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    }, revealOptions);

    reveals.forEach(reveal => {
        revealObserver.observe(reveal);
    });

    // Form submission
    const form = document.getElementById('lead-form');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const submitText = document.getElementById('submit-text');
            const submitSpinner = document.getElementById('submit-spinner');
            const formSuccess = document.getElementById('form-success');
            
            // Basic validation
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const phone = document.getElementById('phone').value;
            const privacy = document.getElementById('privacy').checked;
            
            if (!name || !email || !phone || !privacy) {
                alert('Пожалуйста, заполните все обязательные поля и согласитесь с политикой конфиденциальности.');
                return;
            }

            // Show loading state
            submitText.classList.add('opacity-0');
            submitSpinner.classList.remove('hidden');
            
            // Simulate API call
            try {
                console.log('Sending lead data:', { name, email, phone });
                await new Promise(resolve => setTimeout(resolve, 1500));
                
                // Success
                form.reset();
                formSuccess.classList.remove('hidden');
                
                setTimeout(() => {
                    formSuccess.classList.add('hidden');
                }, 5000);
            } catch (error) {
                console.error('Error submitting form:', error);
                alert('Произошла ошибка при отправке. Пожалуйста, попробуйте позже.');
            } finally {
                // Reset button state
                submitText.classList.remove('opacity-0');
                submitSpinner.classList.add('hidden');
            }
        });
    }
});

// Prodamus integration function
function openPayment() {
    console.log('Redirecting to payment gateway...');
    // In a real scenario, this would redirect to Prodamus or open a widget
    // window.location.href = 'https://yourdomain.payform.ru/...';
    
    // Simulate successful payment redirect for testing
    setTimeout(() => {
        window.location.href = 'success.html';
    }, 500);
}
