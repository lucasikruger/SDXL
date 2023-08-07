def validate_inference(prompt, negative_prompt, num_images_per_prompt, seed, n_steps):
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