```bash
git clone https://github.com/elaird/supy-tflat.git
cd supy-tflat

git clone https://github.com/elaird/supy.git
cd supy
git checkout tweaks
cd ..

source env.sh
ln -s ~/samples-plots/plots_cfg.py .
# edit plots_cfg.py as desired

# edit svSkim.py (listOfSampleDictionaries) as desired
supy svSkim.py --loop 4 --slices=-500 --batch
```
