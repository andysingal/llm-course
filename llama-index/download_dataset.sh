# Clone the repository
git clone https://github.com/AI-Maker-Space/DataRepository.git

# Create the 'source_docs' directory in the current working directory
mkdir source_docs

# Unzip files directly into 'source_docs' directory without preserving internal folder structure
unzip -j "DataRepository/high-performance-rag/Camel Papers Test.zip" -d source_docs
unzip -j "DataRepository/high-performance-rag/Camel Papers Train.zip" -d source_docs

# Delete the cloned repository
rm -rf DataRepository