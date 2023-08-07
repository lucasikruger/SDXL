from PIL import Image

class StableDifussionXL():

    def __init__(self, refiner=False, mem_offload=False):

        self.validate_init(refiner, mem_offload)

    def infer(self, prompt, negative_prompt, num_images_per_prompt =1, seed = None, n_steps=40, use_refiner=False, high_noise_frac=0.8):

        self.validate_inference(prompt,  negative_prompt,num_images_per_prompt,seed, n_steps, use_refiner, high_noise_frac)
        
        result = []
        img1 = Image.open("media/img1.png")
        result.append(img1)
        if num_images_per_prompt > 1:
            img2 = Image.open("media/img2.png")
            result.append(img2)
        
        return result


    def validate_init(self, refiner, mem_offload):
        """
        Validate the init parameters.
        """
        if not isinstance(refiner, bool):
            raise TypeError('refiner must be a boolean')
        if not isinstance(mem_offload, bool):
            raise TypeError('menm_offload must be a boolean')
        
    def validate_inference(self, prompt, negative_prompt, num_images_per_prompt, seed, n_steps, use_refiner, high_noise_frac):
        """
        Validate the inference parameters.
        """
        if not isinstance(prompt, str):
            raise TypeError('prompt must be str')
        if not isinstance(negative_prompt, str):
            raise TypeError('negative_prompt must be str')
        if seed is not None and not isinstance(seed, int):
            raise TypeError('seed must be an int')
        if not isinstance(n_steps, int):
            raise TypeError('n_steps must be an int')
        if not isinstance(num_images_per_prompt, int):
            raise TypeError('num_images_per_prompt must be an int')
        if not (0 < num_images_per_prompt <= 8):
            raise ValueError('num_images_per_prompt must be between 1 and 8')
        if not isinstance(use_refiner, bool):
            raise TypeError('use_refiner must be a boolean')
        if high_noise_frac is not None:
            if not isinstance(high_noise_frac, float):
                raise TypeError('high_noise_frac must be a float')
            if not (0 <= high_noise_frac <= 1):
                raise ValueError('high_noise_frac must be between 0 and 1')