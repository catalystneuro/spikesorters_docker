### To generate (must have matlab compiler):
git clone https://github.com/flatironinstitute/ironclust.git
cd ironclust/matlab
matlab -nosplash -nodisplay -log -r 'irc mcc; quit;'
mv run_irc.app ../../
cd ../..
rm -rf ironclust
