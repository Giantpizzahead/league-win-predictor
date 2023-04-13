run:
	python predict/overlay_predict_windows.py

build_app:
	pip install pyinstaller
	pyinstaller --name "League Win Predictor" --icon icon.ico \
				--add-data "model.gz;." --add-data "data/champ_cache/champ_ratings.pkl;data/champ_cache" \
				--clean --noconfirm predict/overlay_predict_windows.py

.PHONY: run build_app
