    window.onload = function() {
        const title = document.getElementById("titleInput").value;
        const prompt = document.getElementById("promptInput").value;
        const description = document.getElementById("descriptionInput").value;
        const background_image = document.getElementById("background_imageInput").value;

        document.getElementById("titleDisplay").value = title;
        document.getElementById("promptDisplay").value = prompt;
        document.getElementById("distributeDisplay").value = description;

        if (background_image) {
            document.getElementById("backgroundImagePreview").src = background_image;
            document.getElementById("background_imageInputDisplay").value = background_image;

            const link = document.getElementById("backgroundImageLink");
            link.href = background_image;
            link.textContent = background_image;
        }
    };