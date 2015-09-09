all:
	@make -s test > log
	@paste correct log >> logall

all2:
	@make -s test2 > log
	@paste correct log >> logall2


test:
	@for file in *.txt; do ../random_lines $$file | ../text_cat; done

test2:
	@for file in *.txt; do ../text_cat $$file; done
