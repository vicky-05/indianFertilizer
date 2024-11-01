function selectUnit(button) {
    // Remove 'selected' class from all buttons
    const unitButtons = document.querySelectorAll('.unit-btn');
    unitButtons.forEach(btn => btn.classList.remove('selected'));

    // Add 'selected' class to the clicked button
    button.classList.add('selected');
}
document.getElementById('viewAllReviewsBtn').addEventListener('click', function () {
    const hiddenReviews = document.querySelectorAll('.hidden-review');
    hiddenReviews.forEach(review => review.style.display = 'block');
    this.style.display = 'none'; // Hide the button after showing all reviews
});
function changeImage(thumbnail) {
    document.getElementById('mainImage').src = thumbnail.src;
}
let selectedRating = 0;

function setRating(rating) {
    selectedRating = rating;
    document.getElementById('ratingValue').value = rating;
    const stars = document.querySelectorAll('.star');
    stars.forEach((star, index) => {
        star.style.color = index < rating ? '#ffc107' : '#e4e5e9'; // Yellow for selected stars, gray for unselected
    });
}

function submitRating() {
    const feedback = document.getElementById('feedback').value;
    const imageInput = document.getElementById('productImage').files[0];

    if (selectedRating === 0 || !feedback) {
        alert('Please provide a rating and feedback.');
        return;
    }

    // Here you can handle form submission, e.g., send data to a server or store it
    alert(`Rating: ${selectedRating} stars\nFeedback: ${feedback}\nImage: ${imageInput ? imageInput.name : 'No image uploaded'}`);

    // Close the modal after submission
    $('#rateProductModal').modal('hide');
    document.getElementById('ratingForm').reset();
    selectedRating = 0; // Reset rating
    setRating(0); // Reset stars
}


