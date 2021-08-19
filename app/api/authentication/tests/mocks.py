# User mock
user_one = {
    "username": "Ian",
    "email": "ian@example.com",
    "password": "String@123",
    "first_name": "Ian",
    "last_name": "Ian",
    "image": "https://image.jpg",
    "phone_number": "+25470019193"}


# Mutations

admin_signup_mutation = """mutation createAdmin {
  createAdmin(admin:{
    username: "Admin"
    password:"String@123"
    email:"test-email@gmail.com"
    firstName:"Admin"
    lastName:"Kiptoo"
    phoneNumber:"+254743542155"
   image:"https://res.cloudinary.com/dsw3onksq/image/upload/v1592728825/user_x89zcm.png"
  }
  agency:{
    name:"Samar Insurance"
    officeLocation:"Old Mutual"
    boxNumber: 1199
    postalCode:1000
    phoneNumber: "+254727737885"
    agencyEmail:"samar-test@actserv.co.ke"
    imageUrl:"https://res.cloudinary.com/dsw3onksq/image/upload/v1592728825/user_x89zcm.png"
  }){
    status
    message
    admin {
      id
      username
      email
      firstName
      isSuperuser
      isActive
      isStaff
      image
      phoneNumber
      roles
      agency {
        id
        name
        officeLocation
        imageUrl
        agencyEmail
        postalCode
        boxNumber
        isActive
      }
    }
  }
}"""

user_signup_mutation = """mutation createUser {
  createUser(input: {
    username: "Jane",
    email: "jane@example.com",
    password: "String@123",
    firstName: "Doe",
    lastName:"John",
    image:"https://image.jpg",
    phoneNumber:"+254700191910"}) {
    status
    message
    user {
      id
      username,
      firstName,
      email,
      isActive,
      isSuperuser
      roles
      agency {
        id
        name}
    }}}"""

update_user_mutation = """
     mutation updateUser {
      updateUser(input: {
        password: "Pass123@",
        firstName: "Test",
        image:"https://farm4.staticflickr.com/3894/15008518202_c265dfa55f_h.jpg",
        lastName:"Test2",
      }) {
        status
        user {
          id
          username,
          firstName,
          email,
          isActive,
          isSuperuser
        }}}"""

admin_login_mutation = """mutation {
  tokenAuth (
    username: "Admin"
    password:"String@123")
  {payload,
    token
    user {
      id
    }}}"""

user_login_mutation = """mutation {
  tokenAuth (
    email: "ian@example.com",
    password:"String@123")
  {payload,
    token
    user {
      id
    }}}"""
# Queries
users_retrieve_query = """query getUsers {
            users {
            id
            username,
            firstName,
            email,
            isActive,
            isSuperuser}}"""

get_single_user_query = ''' query getUser($id: String!) {
          user(id: $id){
            createdAt
            username
            lastName
            email
            roles}}'''
list_users_query = '''query getUsers {
    users
    {items{
        createdAt
        isSuperuser
        id
        deletedAt
        roles
        firstName
        lastName
        email
        username
        agency{
          id
          name}}
      page
      count
      pages
      hasNext
      hasPrev
    }}'''
roles_query = '''query getRoles {
    roles
  }'''

permission_query= '''query getRolePermissions {
    rolePermissions(role:"Manager")
  }'''