const navSlide = () => {
    const lines = document.querySelector('.lines');
    const nav = document.querySelector('.nav_links');
    const navLinks = document.querySelectorAll('.nav_links li');

    lines.addEventListener('click', () => {
        //  toggle για να παρει την κλάση του active το menu και να εμφανιστεί το πλαινό μενου
        nav.classList.toggle('nav_active');

        // animate για το menubar, και η if για να αναγνωρίζει και να γίνεται το fade καθε φορα που ανοιγει το menu, οχι μονο την 1η
        navLinks.forEach((link, index) => {
            // αν υπάρχει το animation το "διαγραφω" για να ξαναγινει την επομενη φορα
            if (link.style.animation) {
                link.style.animation = ''
            } else {
                // Για να μπαινουν ομαλα τα link που οδηγουν στις αλλες σελιδες με μια καθυστερηση αρχικη για να μπορει να 
                //φανει το fade και ενδιάμεσα στο καθε ενα, και με προσθηκη και αλλων γινεται αυτοματα το delay και σε αυτα
                link.style.animation = `navLinkFade 0.4s ease forwards ${index / 6 + 0.4}s`;
            }
        })

        // κανω toggle το closenav για την δημιουργια x που οταν το πατας και κλεινει το πλαινο μενου.
        lines.classList.toggle('closenav');
    });
}

navSlide();