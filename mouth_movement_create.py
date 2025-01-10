from PIL import Image, ImageDraw

def create_mouth_variation(base_image_path, output_path, mouth_shape):
    # Open the base avatar image
    avatar = Image.open(base_image_path)
    draw = ImageDraw.Draw(avatar)

    ## Define mouth coordinates (adjust as needed)
    if mouth_shape == 'open':
        draw.ellipse([480, 680, 710, 780], fill='black')  # Oval for open mouth
    elif mouth_shape == 'closed':
        draw.rectangle([470, 720, 720, 750], fill='black')  # Line for closed mouth
    elif mouth_shape == 'round':
        draw.ellipse([460, 680, 720, 800], fill='black')  # Circle for round mouth

    # if mouth_shape == 'open':
    #     draw.ellipse([210, 250, 280, 350], fill='red')  # Oval for open mouth
    # elif mouth_shape == 'closed':
    #     draw.rectangle([200, 300, 300, 320], fill='red')  # Line for closed mouth
    # elif mouth_shape == 'round':
    #     draw.ellipse([200, 250, 300, 350], fill='red')  # Circle for round mouth

    # Save the new image
    avatar.save(output_path)

# Example usage
create_mouth_variation('avatar.png', 'mouth_open.png', 'open')
create_mouth_variation('avatar.png', 'mouth_closed.png', 'closed')
create_mouth_variation('avatar.png', 'mouth_round.png', 'round')