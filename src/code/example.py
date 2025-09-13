def verify_relayable_signature(public_key, doc, signature):
    """
    Verify the signed XML elements to have confidence that the claimed
    author did actually generate this message.
    """
    decoded_signature = b64decode(signature)
    rsa_key = RSA.importKey(public_key)
    cipher = PKCS1_v1_5.new(rsa_key)
    sig_hash = _create_signature_hash(doc, 15)
    return cipher.verify(sig_hash, decoded_signature)