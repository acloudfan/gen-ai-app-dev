!bash

echo "Getting the setup script ..."
git clone https://github.com/acloudfan/gen-ai-app-dev.git --quiet

echo "Creating utils folder ..."
mv ./gen-ai-app-dev/utils ./utils
rm -rf gen-ai-app-dev

echo "installing common packages ..."
pip install matplotlib=3.8.4  python-dotenv=0.21.0 

echo "Done"