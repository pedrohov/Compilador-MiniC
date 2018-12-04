int main() {
	int num, div, resto;
	scan("Entre com o inteiro: ", num);
	print(num, " = ");

	// Procura e imprime os fatores:
	while (num > 1) {

		// Encontra o menor fator:
<<<<<<< HEAD
		for (div = 2; num % div; div = div + 1);
=======
		for (div = 2; num % div != 0; div = div + 1);
>>>>>>> e6359c482db1c914a4cedb8db04305e256174029

		print(div);
		num = num / div;
		
		if (num > 1)
			print(" * ");

	}

	print("\n");
	return 0;
} 
