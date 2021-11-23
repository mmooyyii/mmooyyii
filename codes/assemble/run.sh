as -o main.o $1
ld -s -o main main.o
./main
echo Process finished with exit code $?
rm main
rm main.o