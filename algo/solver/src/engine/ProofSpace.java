package engine;

import java.util.ArrayList;
import java.util.List;

/**
 * Collection of statements linked by inferences.
 * @author levat
 *
 */
public class ProofSpace {
	/**
	 * List of inferred statements and premises in the current proof.
	 */
	private List<Statement> statements;

	/**
	 * List of inferences between statements in the proof space.
	 */
	private List<Inference> inferences;

	/**
	 * Stores the indices of all premises.
	 */
	private List<Integer> premises;

	/**
	 * Creates an empty proof space.
	 */
	public ProofSpace() {
		statements = new ArrayList<Statement>();
		inferences = new ArrayList<Inference>();
		premises = new ArrayList<Integer>();
	}

	/*
	 * Creates a proof space and adds premises.
	 */
	public ProofSpace(List<Statement> premises) {
		inferences = new ArrayList<Inference>();
		this.premises = new ArrayList<Integer>();
		statements = new ArrayList<Statement>();
		statements.addAll(premises);

		// Add all premise indices
		for (int i = 0; i < premises.size(); i++) {
			this.premises.add(i);
		}
	}
	
	/**
	 * TEMPORARY: Just tries all the inferences in order.
	 */
	public void infer() {
		deMorgan();
		decomposition();
		modusPonens();
		conditionalDisjunction();
		disjunctiveSyllogism();
	}
	
	/**
	 * The inference rule P, P -> Q implies Q
	 */
	public void modusPonens() {
		for (int i = 0; i < statements.size(); i++) {
			Statement statement = getStatement(i);

			if (statement.getType().equals("IMPLIES")) {
				Statement P = statement.getData().getFirst();
				Statement Q = statement.getData().getSecond();

				int P_location = search(P);

				if (P_location != -1) {
					int Q_location = addStatement(Q);
					addInference(
							new Inference(this, new int[] { P_location, indexOf(statement) }, Q_location, "MODPON"));
				}
			}
		}
	}
	
	/**
	 * The inference rule P | Q, ~P implies Q.
	 */
	public void disjunctiveSyllogism() {
		for (int i = 0; i < statements.size(); i++) {
			Statement statement = getStatement(i);

			if (statement.getType().equals("OR")) {
				Statement P = statement.getData().getFirst();
				Statement Q = statement.getData().getSecond();

				int notP_location = search(new Statement(P).removeDoubleNegatives());

				if (notP_location != -1) {
					int loc = addStatement(Q);
					addInference(new Inference(this, new int[] { indexOf(statement), notP_location }, loc, "DISSYLL"));
					continue;
				}

				int notQ_location = search(new Statement(Q).removeDoubleNegatives());

				if (notQ_location != -1) {
					int loc = addStatement(P);
					addInference(new Inference(this, new int[] { indexOf(statement), notQ_location }, loc, "DISSYLL"));
					continue;
				}
			}
		}
	}
	
	/**
	 * The inference rule P ^ Q implies P,Q.
	 */
	public void decomposition() {
		for (int i = 0; i < statements.size(); i++) {
			Statement statement = getStatement(i);

			if (statement.getType().equals("AND")) {
				Statement P = statement.getData().getFirst();
				Statement Q = statement.getData().getSecond();

				int loc_P = addStatement(P);
				int loc_Q = addStatement(Q);
				
				addInference(new Inference(this, new int[] { indexOf(statement) }, loc_P, "DECOMP"));
				addInference(new Inference(this, new int[] { indexOf(statement) }, loc_Q, "DECOMP"));
			}
		}
	}
	
	/**
	 * The inference rule P -> Q implies ~P | Q.
	 */
	public void conditionalDisjunction() {
		for (int i = 0; i < statements.size(); i++) {
			Statement statement = getStatement(i);

			if (statement.getType().equals("IMPLIES")) {
				Statement P = statement.getData().getFirst();
				Statement Q = statement.getData().getSecond();
				
				int loc = addStatement(new Statement(new Statement(P).removeDoubleNegatives(), Q, "OR"));
				addInference(new Inference(this, new int[] { indexOf(statement) }, loc, "CONDDIS"));
			}
		}
	}
	
	/**
	 * The inference rules:
	 * 
	 * 		1. ~(P + Q) iff ~P ^ ~Q.
	 * 		2. ~(P ^ Q) iff ~P + ~Q.
	 */
	public void deMorgan() {
		for (int i = 0; i < statements.size(); i++) {
			Statement statement = getStatement(i);

			if (statement.getType().equals("NOT")) {
				if (!statement.getData().getFirst().isAtomic()) {
					Statement interior = statement.getData().getFirst();
					Statement P = interior.getData().getFirst();
					Statement Q = interior.getData().getSecond();
					
					String connective_type = "";
					
					if (interior.getType().equals("OR")) {
						connective_type = "AND";
					} else if (interior.getType().equals("AND")) {
						connective_type = "OR";
					}
					
					int loc = addStatement(new Statement(new Statement(P).removeDoubleNegatives(), new Statement(Q).removeDoubleNegatives() , connective_type));
					addInference(new Inference(this, new int[] { indexOf(statement) }, loc, "DEMORG"));
				}
			} else if (statement.getType().equals("OR") || statement.getType().equals("AND")) {
				//if ()
			}
		}
	}
	
	/**
	 * Searches for the statement in the proof space, possibly using 
	 * double negative or associativity rules in the process. Returns -1 if 
	 * the statement was not found.
	 */
	public int search(Statement search) {
		Statement search_DNFree = search.removeDoubleNegatives();
		
		for (int i = 0; i < statements.size(); i++) {
			Statement statement = getStatement(i);
			Statement statement_DNFree = statement.removeDoubleNegatives();
			
			if (search.equals(statement)) {
				return i;
			} else if (search_DNFree.equals(statement_DNFree)) {
				int loc = addStatement(search);
				addInference(new Inference(this, i, loc, "DOUBNEG"));
				
				return loc;
			}
		}
			
		return -1;
	}
	
	public void addInference(Inference inference) {
		if (!inferences.contains(inference)) {
			inferences.add(inference);
		}
	}
	
	/**
	 * Adds the statement to the proof space returning the index. If the statement
	 * already exists within the proof space, it returns the existing index.
	 */
	public int addStatement(Statement statement) {
		if (!statements.contains(statement)) {
			statements.add(statement);
		}
		
		return indexOf(statement);
	}
	
	public int indexOf(Statement statement) {
		return statements.indexOf(statement);
	}
	
	/**
	 * Returns the statement in the proof space with a given index.
	 */
	public Statement getStatement(int index) {
		return statements.get(index);
	}
	
	/**
	 * Adds a premise to the proof space.
	 */
	public void addPremise(Statement statement) {
		int loc = addStatement(statement);
		premises.add(loc);
	}

	/**
	 * Adds the parsed premise to the proof space.
	 */
	public void addPremise(String statement) {
		addPremise(Statement.parse(statement));
	}
	
	/**
	 * Prints the entire contents of the proof space.
	 */
	public String toString() {
		String output = "";

		for (int i = 0; i < premises.size(); i++) {
			output += premises.get(i) + ". " + getStatement(premises.get(i)).toPrintString() + "   |   Premise\r\n";
		}

		for (int i = 0; i < inferences.size(); i++) {
			Inference inference = inferences.get(i);

			output += inference.getTerminal() + ". " + inference.toString() + "\r\n";
		}

		return output;
	}

}
