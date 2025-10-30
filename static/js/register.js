document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    form.addEventListener('submit', (e) => {
        const inputs = form.querySelectorAll('input[required]');
        let valid = true;
        inputs.forEach(input => {
            if (input.value.trim() === '') valid = false;
        });
        if (!valid) {
            e.preventDefault();
            alert('Please fill all required fields!');
        }
    });
});
