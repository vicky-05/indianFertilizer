let selectedRating = 0;

function changeImage(thumbnail) {
    document.getElementById('mainImage').src = thumbnail.src;
}

function setRating(rating) {
    selectedRating = rating;
    document.getElementById('ratingValue').value = rating;
    const stars = document.querySelectorAll('.star');
    stars.forEach((star, index) => {
        star.style.color = index < rating ? '#ffc107' : '#e4e5e9'; // Yellow for selected stars, gray for unselected
    });
}
