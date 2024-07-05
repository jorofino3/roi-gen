package engine;


/**
 * Primitive statement defined by a single letter.
 *
 */
public class AtomicStatement extends Statement {
	
	/**
	 * The name of the atomic statement.
	 */
	private String name;

	/**
	 * Creates an atomic statement with a given name.
	 * 
	 * @param name - the name of the atomic statement.
	 */
	public AtomicStatement(String name) {
		super();
		this.name = name;
	}
	
	@Override
	public boolean equals(Statement statement) {
		return statement.equals(this);
	}
	
	@Override
	public boolean equals(AtomicStatement statement) {
		return name.equals(statement.getName());
	}
	
	@Override
	public boolean isAtomic() {
		return true;
	}
	
	@Override
	public Statement removeDoubleNegatives() {
		return this;
	}
	
	@Override
	public String toPrintString() {
		return toString();
	}
	
	@Override
	public Statement toAssociativeForm() {
		return this;
	}
	
	@Override
	public String toString() {
		return this.name;
	}
	
	public String getName() {
		return name;
	}
	
}
