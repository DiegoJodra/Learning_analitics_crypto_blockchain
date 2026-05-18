import hashlib


def calculate_hash(data_string):
    return hashlib.sha256(data_string.encode()).hexdigest()


def create_block(record, previous_hash):
    block_data = (
        f"{record['student_id']}-"
        f"{record['course']}-"
        f"{record['grade']}-"
        f"{record['participation']}-"
        f"{record['assignments_submitted']}-"
        f"{record['absences']}-"
        f"{record['forum_posts']}-"
        f"{previous_hash}"
    )

    current_hash = calculate_hash(block_data)

    return {
        "student_id": record["student_id"],
        "course": record["course"],
        "grade": record["grade"],
        "participation": record["participation"],
        "assignments_submitted": record["assignments_submitted"],
        "absences": record["absences"],
        "forum_posts": record["forum_posts"],
        "previous_hash": previous_hash,
        "current_hash": current_hash,
    }


def build_blockchain(data):
    blockchain = []
    previous_hash = "0"

    for _, row in data.iterrows():
        block = create_block(row, previous_hash)
        blockchain.append(block)
        previous_hash = block["current_hash"]

    return blockchain


def verify_blockchain(blockchain):
    previous_hash = "0"

    for block in blockchain:
        block_data = (
            f"{block['student_id']}-"
            f"{block['course']}-"
            f"{block['grade']}-"
            f"{block['participation']}-"
            f"{block['assignments_submitted']}-"
            f"{block['absences']}-"
            f"{block['forum_posts']}-"
            f"{previous_hash}"
        )

        recalculated_hash = calculate_hash(block_data)

        if block["previous_hash"] != previous_hash:
            return False

        if block["current_hash"] != recalculated_hash:
            return False

        previous_hash = block["current_hash"]

    return True
