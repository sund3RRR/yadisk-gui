for file in form/*.ui; do
	pyuic6 -x $file -o "${file%.*}.py"
done