
CONFIG = {
    'object directory'   : 'F:/Documents/GitHub/CS-2017-Project/cleaning/29objects',
    'training directory' : 'F:/Documents/GitHub/CS-2017-Project/cleaning/concatenated-images',
    'testing directory'  : 'F:/Documents/GitHub/CS-2017-Project/cleaning/test-images',
    'card directory'     : 'F:/Documents/GitHub/CS-2017-Project/cleaning/card-images',
    
    'card image size'    : (600, 600),
    'card border size'   : (50, 50, 50, 50),
    'card border colour' : (255, 255, 255),
    'card back colour'   : (150, 150, 150),
    
    'pre image size'   : (600, 600),
    'post image size'  : (100, 50),
    
    'truth multiplier' : 4,
    'false samples'    : 200,

    'learning rate'    : 1e-4,
    'epochs'           : 30,
    'output'           : 2,

    'network name'     : 'simplenetv2'
}

MODEL_NAME = 'models/%s-%sLR-%sxT-%sFS-%sEP.model' % (
    CONFIG['network name'],
    CONFIG['learning rate'],
    CONFIG['truth multiplier'],
    CONFIG['false samples'],
    CONFIG['epochs']
)
