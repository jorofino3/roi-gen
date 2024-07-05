package engine;

/**
 * Represents one of the primitive logical connectives: AND, OR, NOT, IMPLIES,
 * IFF
 */
public class LogicalConnective {

	private Statement first, second;
	private String connective_type;

	public LogicalConnective(Statement first, Statement second, String type) {
		this.first = first;
		this.second = second;

		this.connective_type = type;
	}

	/**
	 * Compares logical connectives with commutativity.
	 */
	public boolean equals(LogicalConnective connective) {
		if (connective == null) {
			return false;
		}
		if (connective_type.equals(connective.connective_type)) {

			LogicalConnective current = this.toAssociativeForm();
			LogicalConnective compare = connective.toAssociativeForm();

			if (current.first.equals(compare.first) && current.second.equals(compare.second)) {
				return true;
			}

			if (isCommutative() && current.first.equals(compare.second) && current.second.equals(compare.first)) {
				return true;
			}

			return false;
		} else {
			return false;
		}
	}

	/**
	 * Returns the default associative form of the connective.
	 */
	public LogicalConnective toAssociativeForm() {
		if (isAssociative()) {
			if (!first.isAtomic()) {
				if (first.getType().equals(getType())) {
					return this;
				}
			}

			if (!second.isAtomic()) {
				if (second.getType().equals(getType())) {
					return new LogicalConnective(
							new Statement(first, second.getData().getFirst().toAssociativeForm(), getType()),
							second.getData().getSecond().toAssociativeForm(), getType());
				}
			}
		}

		return this;
	}

	/**
	 * Returns whether or not the logical connective is commutative.
	 */
	public boolean isCommutative() {
		if (connective_type.equals("IMPLIES")) {
			return false;
		}

		return true;
	}

	/**
	 * Returns whether or not the logical connective is associative.
	 */
	public boolean isAssociative() {
		if (connective_type.equals("IMPLIES") || connective_type.equals("NOT")) {
			return false;
		}

		return true;
	}

	@Override
	public String toString() {
		if (connective_type.equals("NOT")) {
			return toPrintString();
		} else {
			return "(" + toPrintString() + ")";
		}
	}

	public String toPrintString() {
		switch (connective_type) {
		case ("AND"):
			return first.toString() + " ^ " + second.toString();
		case ("OR"):
			return first.toString() + " + " + second.toString();
		case ("IMPLIES"):
			return first.toString() + " -> " + second.toString();
		case ("IFF"):
			return first.toString() + " <-> " + second.toString();
		case ("NOT"):
			if (first.isAtomic() || first.getData().getType().equals("NOT")) {
				return "~" + first.toString();
			} else {
				return "~" + first.toString() + "";
			}
		}

		return "";
	}

	public String getType() {
		return this.connective_type;
	}

	public Statement getFirst() {
		return first;
	}

	public Statement getSecond() {
		return second;
	}
}
