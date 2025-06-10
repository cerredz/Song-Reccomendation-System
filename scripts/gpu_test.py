import tensorflow as tf

print("TensorFlow version:", tf.__version__)
print("Built with CUDA:", tf.test.is_built_with_cuda())
print("GPUs:", tf.config.list_physical_devices('GPU'))

# Test if GPU is available
if tf.config.list_physical_devices('GPU'):
    print("✅ GPU detected! Testing computation...")
    # Set memory growth to avoid allocating all GPU memory
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError as e:
            print(e)
    
    # Simple GPU test
    with tf.device('/GPU:0'):
        a = tf.random.normal([1000, 1000])
        b = tf.random.normal([1000, 1000])
        c = tf.matmul(a, b)
    print("✅ GPU computation successful!")
    print("GPU details:", tf.config.list_physical_devices('GPU')[0])
else:
    print("❌ No GPU detected") 