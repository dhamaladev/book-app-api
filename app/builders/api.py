SUCCESS = 1

# Invalid input
INVALID_INPUT = 100
TOO_MANY_REQUEST = 101
EMAIL_OR_PASSWORD_NOT_CORRECT = 343


# User
INVALID_LOGIN_TOKEN = 300
UNAUTHORIZED = 301
USER_NOT_FOUND = 302
INVALID_PASSWORD = 303
ADMIN_USER_NOT_FOUND = 304
PHONE_ALREADY_EXISTS = 307
EMAIL_ALREADY_EXISTS = 308
INVALID_UUID = 409

# Book
BOOK_NOT_FOUND = 400
BOOK_ALREAY_REVIEWD_BY_A_SPECIFIC_USER = 566



error_messages = {
    INVALID_INPUT: "Invalid input",
    TOO_MANY_REQUEST: "Too many requests",
    INVALID_LOGIN_TOKEN: "Invalid token for login",
    UNAUTHORIZED: "Unauthorized",
    EMAIL_OR_PASSWORD_NOT_CORRECT: "Invalid login credentials",
    INVALID_PASSWORD: "Invalid password",
    USER_NOT_FOUND: "user not found",
    BOOK_NOT_FOUND: "book not found",
    INVALID_UUID: "book with id not found",
    BOOK_ALREAY_REVIEWD_BY_A_SPECIFIC_USER: "you have already reviewed this book",
    EMAIL_ALREADY_EXISTS: "User already exists with this email",
}
