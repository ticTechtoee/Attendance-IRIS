document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM content loaded');
    const video = document.getElementById('video');
    const captureButton = document.getElementById('snap');

    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            console.log('getUserMedia succeeded');
            video.srcObject = stream;
        })
        .catch((error) => {
            console.error('Error accessing webcam:', error);
        });

    captureButton.addEventListener('click', function () {
        console.log('Capture button clicked');
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        const imageData = canvas.toDataURL('image/png');

        $.ajax({
            url: '/detect_person/',
            method: 'POST',
            data: { image_data: imageData },
            success: function (response) {
                console.log('Image captured and saved!');
                if (response.success) {
                    console.log('Attendance Marked Successfully');
                    window.location.href = '/attendance_success/';
                } else {
                    console.log('Attendance Not Marked Successfully');
                    window.location.href = '/attendance_fail/';
                }
            },
            error: function (error) {
                console.error('Error capturing image:', error);
            }
        });
    });
});