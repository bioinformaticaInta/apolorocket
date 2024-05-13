CREATE TABLE reference(
	id INT GENERATED ALWAYS AS IDENTITY,
	genus VARCHAR(50) NOT NULL,
	specie VARCHAR(50) NOT NULL,
	version VARCHAR(50) NOT NULL,
	annotation BOOLEAN NOT NULL DEFAULT false,
	genomic BOOLEAN NOT NULL,
	UNIQUE(genus, specie, genomic, version),
	PRIMARY KEY(id)
);
CREATE TABLE reference_region(
	id INT GENERATED ALWAYS AS IDENTITY,
	reference_id INT,
	sequence_name text NOT NULL,
	start_position INT NOT NULL,
	end_position INT NOT NULL,
	annotation TEXT,
	UNIQUE(reference_id, sequence_name, start_position, end_position),
	PRIMARY KEY(id),
	CONSTRAINT fk_tr_reference
		FOREIGN KEY(reference_id)
			REFERENCES reference(id)
);
CREATE TABLE reference_region_block(
	id INT GENERATED ALWAYS AS IDENTITY,
	reference_region_id INT,
	start_position INT NOT NULL,
	end_position INT NOT NULL,
	UNIQUE(reference_region_id, start_position, end_position),
	PRIMARY KEY(id),
	CONSTRAINT fk_trb_reference_region
		FOREIGN KEY(reference_region_id)
			REFERENCES reference_region(id)
);
CREATE TABLE query(
	id INT GENERATED ALWAYS AS IDENTITY,
	name TEXT NOT NULL,
	sequence TEXT NOT NULL,
	UNIQUE(name),
	UNIQUE(sequence),
	PRIMARY KEY(id)
);
CREATE TABLE query_region(
	id INT GENERATED ALWAYS AS IDENTITY,
	query_id INT,
	start_position INT NOT NULL,
	end_position INT NOT NULL,
	UNIQUE(query_id, start_position, end_position),
	PRIMARY KEY(id),
	CONSTRAINT fk_qr_query
		FOREIGN KEY(query_id)
			REFERENCES query(id)
);
CREATE TABLE query_region_block(
	id INT GENERATED ALWAYS AS IDENTITY,
	query_region_id INT,
	start_position INT NOT NULL,
	end_position INT NOT NULL,
	UNIQUE(query_region_id, start_position, end_position),
	PRIMARY KEY(id),
	CONSTRAINT fk_qb_query_region
		FOREIGN KEY(query_region_id)
			REFERENCES query_region(id)
);
CREATE TABLE alignment(
	id INT GENERATED ALWAYS AS IDENTITY,
	query_region_block_id INT,
	reference_region_block_id INT,
	strand CHAR,
	missmatches INT,
	alignment_block_number INT,
	UNIQUE(query_region_block_id, reference_region_block_id, strand, missmatches, alignment_block_number),
	PRIMARY KEY(id),
	CONSTRAINT fk_a_query_region_block
		FOREIGN KEY(query_region_block_id)
			REFERENCES query_region_block(id),
	CONSTRAINT fk_a_reference_region_block
		FOREIGN KEY(reference_region_block_id)
			REFERENCES reference_region_block(id)
);
CREATE TABLE efficiency(
	id INT GENERATED ALWAYS AS IDENTITY,
	query_id INT,
	method VARCHAR(50) NOT NULL,
	efficiency_data INT[] NOT NULL,
	UNIQUE(query_id, method, efficiency_data),
	PRIMARY KEY(id),
	CONSTRAINT fk_e_query
		FOREIGN KEY(query_id)
			REFERENCES query(id)
);
CREATE TABLE project(
	id INT GENERATED ALWAYS AS IDENTITY,
	name VARCHAR(50) NOT NULL,
	description TEXT,
	genus VARCHAR(50) NOT NULL,
	specie VARCHAR(50) NOT NULL,
	user_name VARCHAR(50) NOT NULL,
	initial_date DATE NOT NULL,
	last_modification_date DATE,
	UNIQUE(name),
	PRIMARY KEY(id)
);
CREATE TABLE maintarget_comparison(
	id INT GENERATED ALWAYS AS IDENTITY,
	project_id INT,
	query_region_id INT,
	PRIMARY KEY(id),
	CONSTRAINT fk_mtc_project
		FOREIGN KEY(project_id)
			REFERENCES project(id),
	CONSTRAINT fk_mtc_query_region
		FOREIGN KEY(query_region_id)
			REFERENCES query_region(id)
);
CREATE TABLE maintarget_comparison_reference(
	id INT GENERATED ALWAYS AS IDENTITY,
	maintarget_comparison_id INT,
	reference_id INT,
	UNIQUE(maintarget_comparison_id, reference_id),
	PRIMARY KEY(id),
	CONSTRAINT fk_mtcr_maintarget_comparison
		FOREIGN KEY(maintarget_comparison_id)
			REFERENCES maintarget_comparison(id),
	CONSTRAINT fk_mtcr_reference
		FOREIGN KEY(reference_id)
			REFERENCES reference(id)
);
CREATE TABLE maintarget_comparison_reference_region(
	id INT GENERATED ALWAYS AS IDENTITY,
	maintarget_comparison_reference_id INT,
	target_number INT NOT NULL,
	reference_region_id INT,
	maintarget BOOLEAN, 
	UNIQUE(maintarget_comparison_reference_id, target_number, reference_region_id),
	PRIMARY KEY(id),
	CONSTRAINT fk_mtcrr_maintarget_comparison_reference
		FOREIGN KEY(maintarget_comparison_reference_id)
			REFERENCES maintarget_comparison_reference(id),
	CONSTRAINT fk_mtcrr_reference_region
		FOREIGN KEY(reference_region_id)
			REFERENCES reference_region(id)
);
CREATE TABLE offtarget_comparison(
	id INT GENERATED ALWAYS AS IDENTITY,
	project_id INT,
	query_region_id INT,
	selected_region BOOLEAN NOT NULL DEFAULT false,
	PRIMARY KEY(id),
	CONSTRAINT fk_otc_project
		FOREIGN KEY(project_id)
			REFERENCES project(id),
	CONSTRAINT fk_otc_query
		FOREIGN KEY(query_region_id)
			REFERENCES query_region(id)
);
CREATE TABLE offtarget_comparison_reference(
	id INT GENERATED ALWAYS AS IDENTITY,
	offtarget_comparison_id INT,
	reference_id INT,
	UNIQUE(offtarget_comparison_id, reference_id),
	PRIMARY KEY(id),
	CONSTRAINT fk_otcr_maintarget_comparison
		FOREIGN KEY(offtarget_comparison_id)
			REFERENCES offtarget_comparison(id),
	CONSTRAINT fk_otcr_reference
		FOREIGN KEY(reference_id)
			REFERENCES reference(id)
);
CREATE TABLE offtarget_comparison_reference_region(
	id INT GENERATED ALWAYS AS IDENTITY,
	offtarget_comparison_reference_id INT,
	target_number INT NOT NULL,
	reference_region_id INT,
	UNIQUE(offtarget_comparison_reference_id, target_number, reference_region_id),
	PRIMARY KEY(id),
	CONSTRAINT fk_otcrr_offtarget_comparison_reference
		FOREIGN KEY(offtarget_comparison_reference_id)
			REFERENCES offtarget_comparison_reference(id),
	CONSTRAINT fk_otcrr_reference_region
		FOREIGN KEY(reference_region_id)
			REFERENCES reference_region(id)
);
