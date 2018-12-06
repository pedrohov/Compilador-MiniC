int main() {
	int i;
	for(i = 0; i < 10; i = i + 1) {
		if(i == 2)
			continue;
		else if(i == 5)
			print(">>Cinco<<\n");
		else
			print(i, "\n");
	}

	return 0;
}