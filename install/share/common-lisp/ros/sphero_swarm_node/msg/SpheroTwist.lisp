; Auto-generated. Do not edit!


(cl:in-package sphero_swarm_node-msg)


;//! \htmlinclude SpheroTwist.msg.html

(cl:defclass <SpheroTwist> (roslisp-msg-protocol:ros-message)
  ((name
    :reader name
    :initarg :name
    :type cl:string
    :initform "")
   (linear
    :reader linear
    :initarg :linear
    :type geometry_msgs-msg:Vector3
    :initform (cl:make-instance 'geometry_msgs-msg:Vector3))
   (angular
    :reader angular
    :initarg :angular
    :type geometry_msgs-msg:Vector3
    :initform (cl:make-instance 'geometry_msgs-msg:Vector3)))
)

(cl:defclass SpheroTwist (<SpheroTwist>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SpheroTwist>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SpheroTwist)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name sphero_swarm_node-msg:<SpheroTwist> is deprecated: use sphero_swarm_node-msg:SpheroTwist instead.")))

(cl:ensure-generic-function 'name-val :lambda-list '(m))
(cl:defmethod name-val ((m <SpheroTwist>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader sphero_swarm_node-msg:name-val is deprecated.  Use sphero_swarm_node-msg:name instead.")
  (name m))

(cl:ensure-generic-function 'linear-val :lambda-list '(m))
(cl:defmethod linear-val ((m <SpheroTwist>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader sphero_swarm_node-msg:linear-val is deprecated.  Use sphero_swarm_node-msg:linear instead.")
  (linear m))

(cl:ensure-generic-function 'angular-val :lambda-list '(m))
(cl:defmethod angular-val ((m <SpheroTwist>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader sphero_swarm_node-msg:angular-val is deprecated.  Use sphero_swarm_node-msg:angular instead.")
  (angular m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SpheroTwist>) ostream)
  "Serializes a message object of type '<SpheroTwist>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'name))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'name))
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'linear) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'angular) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SpheroTwist>) istream)
  "Deserializes a message object of type '<SpheroTwist>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'name) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'name) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'linear) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'angular) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SpheroTwist>)))
  "Returns string type for a message object of type '<SpheroTwist>"
  "sphero_swarm_node/SpheroTwist")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SpheroTwist)))
  "Returns string type for a message object of type 'SpheroTwist"
  "sphero_swarm_node/SpheroTwist")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SpheroTwist>)))
  "Returns md5sum for a message object of type '<SpheroTwist>"
  "d9b209833fd737ccfb12e73a6bc3716e")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SpheroTwist)))
  "Returns md5sum for a message object of type 'SpheroTwist"
  "d9b209833fd737ccfb12e73a6bc3716e")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SpheroTwist>)))
  "Returns full string definition for message of type '<SpheroTwist>"
  (cl:format cl:nil "string name~%geometry_msgs/Vector3 linear~%geometry_msgs/Vector3 angular~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SpheroTwist)))
  "Returns full string definition for message of type 'SpheroTwist"
  (cl:format cl:nil "string name~%geometry_msgs/Vector3 linear~%geometry_msgs/Vector3 angular~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SpheroTwist>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'name))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'linear))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'angular))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SpheroTwist>))
  "Converts a ROS message object to a list"
  (cl:list 'SpheroTwist
    (cl:cons ':name (name msg))
    (cl:cons ':linear (linear msg))
    (cl:cons ':angular (angular msg))
))
