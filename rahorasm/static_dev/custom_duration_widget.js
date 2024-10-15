// js/custom_duration_widget.js
document.addEventListener('DOMContentLoaded', function() {
    const durationInputs = document.querySelectorAll('.duration-widget');
    durationInputs.forEach(input => {
        input.addEventListener('change', function() {
            const hours = Math.floor(this.value / 3600);
            const minutes = Math.floor((this.value % 3600) / 60);
            this.value = `${hours}:${('0' + minutes).slice(-2)}`;
        });
    });
});
