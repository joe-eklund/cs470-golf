// Generated by gencpp from file sphero_swarm_node/SpheroTwist.msg
// DO NOT EDIT!


#ifndef SPHERO_SWARM_NODE_MESSAGE_SPHEROTWIST_H
#define SPHERO_SWARM_NODE_MESSAGE_SPHEROTWIST_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <geometry_msgs/Vector3.h>
#include <geometry_msgs/Vector3.h>

namespace sphero_swarm_node
{
template <class ContainerAllocator>
struct SpheroTwist_
{
  typedef SpheroTwist_<ContainerAllocator> Type;

  SpheroTwist_()
    : name()
    , linear()
    , angular()  {
    }
  SpheroTwist_(const ContainerAllocator& _alloc)
    : name(_alloc)
    , linear(_alloc)
    , angular(_alloc)  {
    }



   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _name_type;
  _name_type name;

   typedef  ::geometry_msgs::Vector3_<ContainerAllocator>  _linear_type;
  _linear_type linear;

   typedef  ::geometry_msgs::Vector3_<ContainerAllocator>  _angular_type;
  _angular_type angular;




  typedef boost::shared_ptr< ::sphero_swarm_node::SpheroTwist_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::sphero_swarm_node::SpheroTwist_<ContainerAllocator> const> ConstPtr;

}; // struct SpheroTwist_

typedef ::sphero_swarm_node::SpheroTwist_<std::allocator<void> > SpheroTwist;

typedef boost::shared_ptr< ::sphero_swarm_node::SpheroTwist > SpheroTwistPtr;
typedef boost::shared_ptr< ::sphero_swarm_node::SpheroTwist const> SpheroTwistConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::sphero_swarm_node::SpheroTwist_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::sphero_swarm_node::SpheroTwist_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace sphero_swarm_node

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': False}
// {'geometry_msgs': ['/opt/ros/jade/share/geometry_msgs/cmake/../msg'], 'sphero_swarm_node': ['/home/theta/catkin_ws/src/sphero_ros/sphero_swarm_node/msg'], 'std_msgs': ['/opt/ros/jade/share/std_msgs/cmake/../msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::sphero_swarm_node::SpheroTwist_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::sphero_swarm_node::SpheroTwist_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::sphero_swarm_node::SpheroTwist_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::sphero_swarm_node::SpheroTwist_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::sphero_swarm_node::SpheroTwist_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::sphero_swarm_node::SpheroTwist_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::sphero_swarm_node::SpheroTwist_<ContainerAllocator> >
{
  static const char* value()
  {
    return "d9b209833fd737ccfb12e73a6bc3716e";
  }

  static const char* value(const ::sphero_swarm_node::SpheroTwist_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xd9b209833fd737ccULL;
  static const uint64_t static_value2 = 0xfb12e73a6bc3716eULL;
};

template<class ContainerAllocator>
struct DataType< ::sphero_swarm_node::SpheroTwist_<ContainerAllocator> >
{
  static const char* value()
  {
    return "sphero_swarm_node/SpheroTwist";
  }

  static const char* value(const ::sphero_swarm_node::SpheroTwist_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::sphero_swarm_node::SpheroTwist_<ContainerAllocator> >
{
  static const char* value()
  {
    return "string name\n\
geometry_msgs/Vector3 linear\n\
geometry_msgs/Vector3 angular\n\
\n\
================================================================================\n\
MSG: geometry_msgs/Vector3\n\
# This represents a vector in free space. \n\
\n\
float64 x\n\
float64 y\n\
float64 z\n\
";
  }

  static const char* value(const ::sphero_swarm_node::SpheroTwist_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::sphero_swarm_node::SpheroTwist_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.name);
      stream.next(m.linear);
      stream.next(m.angular);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER;
  }; // struct SpheroTwist_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::sphero_swarm_node::SpheroTwist_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::sphero_swarm_node::SpheroTwist_<ContainerAllocator>& v)
  {
    s << indent << "name: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.name);
    s << indent << "linear: ";
    s << std::endl;
    Printer< ::geometry_msgs::Vector3_<ContainerAllocator> >::stream(s, indent + "  ", v.linear);
    s << indent << "angular: ";
    s << std::endl;
    Printer< ::geometry_msgs::Vector3_<ContainerAllocator> >::stream(s, indent + "  ", v.angular);
  }
};

} // namespace message_operations
} // namespace ros

#endif // SPHERO_SWARM_NODE_MESSAGE_SPHEROTWIST_H
