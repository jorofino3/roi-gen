package engine;

import java.util.Arrays;

/**
 * Represents an inference between statements.
 */
public class Inference {

	/**
	 * Proof space in which the inference is located.
	 */
	private ProofSpace ambient_space;

	/**
	 * Indices of the hypotheses of the inference.
	 */
	private int[] initial;

	/**
	 * Index of the conclusion of the inference.
	 */
	private int terminal;

	/**
	 * Type of inference. Could be: COMM - Commutativity MODPON - Modus Ponens
	 * DOUBNEG - Double Negative CONDDIS - Conditional Disjunction DISSYLL - Disjunctive
	 * Syllogism
	 * DECOMP - Decomposition
	 * DEMORG - DeMorgan's Laws
	 */
	protected String inference_type;

	public Inference(ProofSpace ambient_space, int[] initial, int terminal, String type) {
		this.ambient_space = ambient_space;
		this.initial = initial;
		this.terminal = terminal;
		this.inference_type = type;
	}

	public Inference(ProofSpace ambient_space, int initial, int terminal, String type) {
		this.ambient_space = ambient_space;
		this.initial = new int[] { initial };
		this.terminal = terminal;
		this.inference_type = type;
	}

	@Override
	public boolean equals(Object object) {
		if (object instanceof Inference) {
			return equals((Inference) object);
		}

		return false;
	}

	public boolean equals(Inference inference) {
		return (inference_type.equals(inference.inference_type) && terminal == inference.getTerminal())
				&& Arrays.equals(initial, inference.initial);
	}

	/**
	 * Converts the inference to a string.
	 */
	public String toString() {
		String initial_string = "";

		for (int i = 0; i < initial.length; i++) {
			initial_string += initial[i];

			if (i != initial.length - 1) {
				initial_string += ", ";
			}
		}

		return ambient_space.getStatement(terminal).toPrintString() + "   |   " + inferenceName(inference_type) + " "
				+ initial_string;
	}

	public String getInferenceName() {
		return inferenceName(this.inference_type);
	}

	private static String inferenceName(String type) {
		switch (type) {
		case "COMM":
			return "Commutativity";
		case "MODPON":
			return "Modus Ponens";
		case "DOUBNEG":
			return "Double Negative";
		case "CONDDIS":
			return "Conditional Disjunction";
		case "DISSYLL":
			return "Disjunctive Syllogism";
		case "DECOMP":
			return "Decomposition";
		case "DEMORG":
			return "DeMorgan's Laws";
		}

		return "";
	}

	public int getInitial(int index) {
		return initial[index];
	}

	public int getTerminal() {
		return terminal;
	}

	public int[] getInitial() {
		return initial;
	}

	public String getType() {
		return inference_type;
	}
}
