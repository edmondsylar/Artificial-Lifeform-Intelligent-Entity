# we are going to start the layer and all it's required modules from this file.

# activate the Environment you are working from
conda activate alfie_base
# star the Conciousnes module
nohup python LayerAutonomy/conciousness.py &> /dev/null &

# start the layer
nohup python GeminiSupport.py &> /dev/null &

# ps