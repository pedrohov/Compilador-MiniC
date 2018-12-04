/****

comentarioembloco
*****/

int main() {
	int num, div, resto;
	scan("Entre com o inteiro: ", num);
	print(num, " = ");

	// Procura e imprime os fatores:
	while (num > 1) {

		// Encontra o menor fator:
		for (div = 2; num % div != 0; div = div + 1);
/*
		print(div);*/
		num = num / div;
		
		if (num > 1)
			print(" * ");

	}

	print("\n");
	return 0;
} 
