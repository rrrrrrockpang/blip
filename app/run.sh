# python fetch.py --data_dir data
# # python fetch_history.py --articles articles.pkl \
# #                         --data_dir data \
# #                         --history 1

# python 01-title-classifier.py --articles data/articles.pkl \
#                         --model_path model \
#                         --output_data_path intermediate/title_filtered_articles.pkl

# python 02-content-classifier.py --input_data_path intermediate/title_filtered_articles.pkl \
#                             --token_keys keys.json \
#                             --output_data_path intermediate/content_filtered_articles.pkl

# python 03-summarizer.py --input_data_path intermediate/content_filtered_articles.pkl \
#                         --token_keys keys.json \
#                         --output_data_path intermediate/summary.pkl

# python 04-aspect-classifier.py --input_data_path intermediate/summary.pkl \
#                             --token_keys keys.json \
#                             --output_data_path intermediate/aspect.pkl
