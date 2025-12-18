# adhoc
cd extracted_api/script
python extract_all_apis.py
python extract_all_wiki_instructions.py

cd ..
python merge_all_apis.py
python generate_centralized_prompt.py --output centralized_prompt.md
cd ..

# adhoc + unclear
cd extracted_api/script
python extract_all_apis_w_SimilarAPIs.py
python extract_all_wiki_instructions_w_SimliarAPIs.py

cd ..
python merge_all_apis_w_SimilarAPIs.py
python generate_centralized_prompt_w_SimilarAPIs.py --output centralized_prompt_unclear.md
cd ..