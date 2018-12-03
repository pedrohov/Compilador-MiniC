int main() {
	
	int n;
	int teste;
	n = 9 * 5 + (-3.5);
	print(n, "\n");

	if(n == 5) {
		print("Hmm\n");
	} else {
		print("Dois\n");
	}

    scan("Teste = ", teste);
    print(teste, "\n");

	int i;
	i = 0;
	while(i < teste) {
		print(i, "\n");
		i = i + 1;
	}

	for(i = 0; i < 10; i = i + 1) {
		if(i > 5)
			teste = 0;
		else if(i == 3)
			break;
		else
			print(i, "\n");
	}
    
    n = teste * (6 + (-3)) / 9;
    print(n, "\n");
    print(teste, "\n");

    return 0;
}