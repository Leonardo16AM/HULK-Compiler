#ifndef ERROR_H
#define ERROR_H
#include <string>


class error {   
public:
    error(const std::string& message) : message_(message) {}
    error(const std::string& message, int row, int col) : message_(message + " at row " + std::to_string(row) + " col " + std::to_string(col)) {}
    
    const std::string& message() const { return message_; }
private:
    std::string message_;
};

#endif
