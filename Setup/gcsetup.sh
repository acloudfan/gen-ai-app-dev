#/bin/!bash

rm -rf ./gen-ai-app-dev > /dev/null
rm ./gcsetup.sh > /dev/null
rm -rf ./utils > /dev/null
rm -rf ./data > /dev/null

echo "Getting the setup script ..."
git clone https://github.com/acloudfan/gen-ai-app-dev.git --quiet

echo "Creating utils folder ..."
mv ./gen-ai-app-dev/utils ./utils



echo "Installing common packages ..."
pip install --quiet matplotlib==3.8.4  python-dotenv==0.21.0 

while getopts "h:l" option; do
    case $option in
        # Install langchain dependencies
        l) 
            echo "Installing Langchain Packages ... "
            pip install --quiet -r  ./gen-ai-app-dev/Setup/langchain-requirements.txt
            ;;
        h)
            echo "Intalling HuggingFace libraries ..."
            pip install --quiet -r  ./gen-ai-app-dev/Setup/huggingface-requirements.txt
            ;;
    esac
done



echo "Done"