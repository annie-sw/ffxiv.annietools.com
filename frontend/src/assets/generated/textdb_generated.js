// automatically generated by the FlatBuffers compiler, do not modify

/**
 * @const
 * @namespace
 */
var Eorzea = Eorzea || {};

/**
 * @constructor
 */
Eorzea.Dummy = function() {
  /**
   * @type {flatbuffers.ByteBuffer}
   */
  this.bb = null;

  /**
   * @type {number}
   */
  this.bb_pos = 0;
};

/**
 * @param {number} i
 * @param {flatbuffers.ByteBuffer} bb
 * @returns {Eorzea.Dummy}
 */
Eorzea.Dummy.prototype.__init = function(i, bb) {
  this.bb_pos = i;
  this.bb = bb;
  return this;
};

/**
 * @param {flatbuffers.ByteBuffer} bb
 * @param {Eorzea.Dummy=} obj
 * @returns {Eorzea.Dummy}
 */
Eorzea.Dummy.getRootAsDummy = function(bb, obj) {
  return (obj || new Eorzea.Dummy).__init(bb.readInt32(bb.position()) + bb.position(), bb);
};

/**
 * @param {flatbuffers.Builder} builder
 */
Eorzea.Dummy.startDummy = function(builder) {
  builder.startObject(0);
};

/**
 * @param {flatbuffers.Builder} builder
 * @returns {flatbuffers.Offset}
 */
Eorzea.Dummy.endDummy = function(builder) {
  var offset = builder.endObject();
  return offset;
};

// Exports for Node.js and RequireJS
this.Eorzea = Eorzea;
