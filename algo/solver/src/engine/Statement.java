package engine;

/**
 * General statement in propositional logic, composed of logical connectives
 * built up from atomic statements.
 */
public class Statement {
	
	/**
	 * If the statement is atomic, this will be null, otherwise this will be a
	 * logical connective representing the root node of the syntatic tree of the
	 * statement.
	 */
	private LogicalConnective data;

	/**
	 * Creates a statement with given data.
	 * 
	 * @param data - logical connective representing the contents of the statement.
	 */
	public Statement(LogicalConnective data) {
		this.data = data;
	}

	/**
	 * Creates a statement with the given data.
	 */
	public Statement(Statement first, Statement second, String connective_type) {
		this.data = new LogicalConnective(first, second, connective_type);
	}

	/**
	 * Creates a statement by parsing the string. Syntax: AND - ^ OR - || NOT - ~
	 * IMPLIES - --> IFF - <-->
	 * 
	 * Each logical connective also enclosed in parenthesis.
	 * 
	 * @param description - string representing the statement.
	 */
	public static Statement parse(String description) {
		// Remove whitespace
		description = description.replace(" ", "");

		String parenthesis = "[(]";

		// Check if atomic
		if (!description.contains(parenthesis) && description.length() == 1) {
			return new AtomicStatement(description);
		}
		// NOT case
		if (description.startsWith("~")) {

			// Remove ~
			description = description.replaceFirst("~", "");

			if (description.startsWith(parenthesis)) {
				// Remove ( )
				description = description.replaceFirst(parenthesis, "");
				description = description.substring(0, description.length() - 1);
			}

			Statement statement = Statement.parse(description);

			return new Statement(statement);
		} else {
			description = description.substring(1, description.length() - 1);

			// Find splitting point
			int split_index = 0;

			if (description.startsWith("(")) {
				int parenthesis_counter = 0;

				for (int i = 0; i < description.length(); i++) {
					char s = description.charAt(i);

					if (s == '(') {
						parenthesis_counter++;
					} else if (s == ')') {
						parenthesis_counter--;
					}

					if (i != 0 && parenthesis_counter == 0) {
						split_index = i;
						break;
					}
				}
			} else {
				String neg = "";

				// Weird case
				if (description.startsWith("~")) {
					neg = "~";

					while (description.replaceFirst(neg, "").startsWith("~")) {
						neg += "~";
					}
				}

				split_index = neg.length();
				
				if (description.charAt(split_index) == '(') {
					int parenthesis_counter = 0;

					for (int i = 0; i < description.length(); i++) {
						char s = description.charAt(i);

						if (s == '(') {
							parenthesis_counter++;
						} else if (s == ')') {
							parenthesis_counter--;
						}

						if (i != 0 && parenthesis_counter == 0) {
							split_index = i;
							break;
						}
					}
				}
			}

			// Figure out type of logical connective
			String connective = Character.toString(description.charAt(split_index + 1));

			if (connective.startsWith("-")) {
				connective = "->";
			} else if (connective.startsWith("<")) {
				connective = "<->";
			}

			Statement first = Statement.parse(description.substring(0, split_index + 1));
			Statement second = Statement
					.parse(description.substring(split_index + 1 + connective.length(), description.length()));

			String connective_type = "";

			switch (connective) {
			case "^":
				connective_type = "AND";
				break;
			case "+":
				connective_type = "OR";
				break;
			case "->":
				connective_type = "IMPLIES";
				break;
			case "<->":
				connective_type = "IFF";
				break;
			}

			return new Statement(first, second, connective_type);
		}
	}

	protected Statement() {
		this.data = null;
	}
	
	/**
	 * NOT statement
	 */
	public Statement(Statement statement) {
		this.data = new LogicalConnective(statement, statement, "NOT");
	}
	
	@Override
	public boolean equals(Object object) {
		if (object instanceof Statement) {
			return equals((Statement) object);
		}
		
		return false;
	}

	public boolean isAtomic() {
		return false;
	}

	public boolean equals(Statement statement) {
		return this.data.equals(statement.data);
	}
	
	public boolean equals(AtomicStatement statement) {
		return false;
	}
	
	/**
	 * Converts the statement into a string.
	 */
	public String toString() {
		return data.toString();
	}

	/**
	 * Converts the statement into a string suitable for displaying.
	 */
	public String toPrintString() {
		return data.toPrintString();
	}

	public LogicalConnective getData() {
		return this.data;
	}

	public String getType() {
		if (this.data == null) {
			return "";
		}
		return this.data.getType();
	}

	/**
	 * Returns the statement, but replacing ~~P with P.
	 */
	public Statement removeDoubleNegatives() {
		if (this.getType().equals("NOT")) {
			if (!this.data.getFirst().isAtomic()) {
				if(this.data.getFirst().getType().equals("NOT")) {
					return this.data.getFirst().getData().getFirst().removeDoubleNegatives();
				}
			}
			
			return this;
		} else {
			return new Statement(this.getData().getFirst().removeDoubleNegatives(),
					this.getData().getSecond().removeDoubleNegatives(), this.getType());
		}
	}
	
	/**
	 * Returns the associative form of the statement.
	 */
	public Statement toAssociativeForm() {
		return new Statement(data.toAssociativeForm());
	}
}
