//============================================================================
// Name        : HashTable.cpp
// Author      : Larissa Rojas
// Version     : 1.0
// Copyright   : Copyright © 2023 SNHU COCE
// Description : Lab 4-2 Hash Table
//============================================================================

#include <algorithm>
#include <climits>
#include <iostream>
#include <string>
#include <time.h>
#include <vector>
#include <functional>   // added for std::hash<string>

#include "CSVparser.hpp"

using namespace std;

// Global definitions visible to all methods and classes

const unsigned int DEFAULT_SIZE = 179;

double strToDouble(string str, char ch);

// define a structure to hold bid information
struct Bid {
    string bidId;
    string title;
    string fund;
    double amount;
    Bid() {
        amount = 0.0;
    }
};

// Hash Table class definition

class HashTable {
private:
    struct Node {
        Bid bid;
        unsigned int key;
        Node* next;

        Node() {
            key = UINT_MAX;
            next = nullptr;
        }

        Node(Bid aBid) : Node() {
            bid = aBid;
        }

        Node(Bid aBid, unsigned int aKey) : Node(aBid) {
            key = aKey;
        }
    };

    vector<Node*> nodes;
    unsigned int tableSize = DEFAULT_SIZE;

    // use string keys so we don't rely on converting to int
    unsigned int hash(const std::string& key);

public:
    HashTable();
    HashTable(unsigned int size);
    virtual ~HashTable();
    void Insert(Bid bid);
    void PrintAll();
    void Remove(string bidId);
    Bid Search(string bidId);
    size_t Size();
};

// Default constructor
HashTable::HashTable() {
    nodes.resize(tableSize, nullptr);
}

// Constructor with size
HashTable::HashTable(unsigned int size) {
    this->tableSize = size;
    nodes.resize(tableSize, nullptr);
}

// Destructor
HashTable::~HashTable() {
    for (unsigned int i = 0; i < nodes.size(); ++i) {
        Node* current = nodes[i];
        while (current != nullptr) {
            Node* temp = current;
            current = current->next;
            delete temp;
        }
    }
}

// hash the string id and mod by table size
unsigned int HashTable::hash(const std::string& key) {
    std::hash<std::string> hasher;
    return static_cast<unsigned int>(hasher(key) % tableSize);
}

// Insert bid
void HashTable::Insert(Bid bid) {
    // use string hash directly (no stoi)
    unsigned int key = hash(bid.bidId);
    Node* newNode = new Node(bid, key);

    if (nodes[key] == nullptr) {
        nodes[key] = newNode;
    }
    else {
        Node* current = nodes[key];
        while (current->next != nullptr) {
            // if we want, we could check for duplicate bidId here
            current = current->next;
        }
        current->next = newNode;
    }
}

// Print all bids (kept as buckets so collisions are visible)
void HashTable::PrintAll() {
    for (unsigned int i = 0; i < nodes.size(); ++i) {
        Node* current = nodes[i];
        while (current != nullptr) {
            cout << "Key " << i << ": " << current->bid.bidId << " | "
                 << current->bid.title << " | " << current->bid.amount << " | "
                 << current->bid.fund << endl;
            current = current->next;
        }
    }
}

// Remove bid
void HashTable::Remove(string bidId) {
    // use string hash (no stoi)
    unsigned int key = hash(bidId);
    Node* current = nodes[key];
    Node* previous = nullptr;

    while (current != nullptr) {
        if (current->bid.bidId == bidId) {
            if (previous == nullptr) {
                nodes[key] = current->next;
            }
            else {
                previous->next = current->next;
            }
            delete current;
            return;
        }
        previous = current;
        current = current->next;
    }
}

// Search bid
Bid HashTable::Search(string bidId) {
    Bid bid;
    // use string hash (no stoi)
    unsigned int key = hash(bidId);
    Node* current = nodes[key];

    while (current != nullptr) {
        if (current->bid.bidId == bidId) {
            return current->bid;
        }
        current = current->next;
    }
    return bid;
}

// Display bid
void displayBid(Bid bid) {
    cout << bid.bidId << ": " << bid.title << " | " << bid.amount << " | " << bid.fund << endl;
}

// Load bids from CSV
void loadBids(string csvPath, HashTable* hashTable) {
    cout << "Loading CSV file " << csvPath << endl;

    csv::Parser file = csv::Parser(csvPath);

    int bidCount = 0;

    try {
        for (unsigned int i = 0; i < file.rowCount(); i++) {
            // simple safety check: skip short/bad rows
            if (file[i].size() <= 8) {
                continue;
            }

            // Create a data structure and add to the collection of bids
            Bid bid;
            bid.bidId  = file[i][1];
            bid.title  = file[i][0];
            bid.fund   = file[i][8];
            bid.amount = strToDouble(file[i][4], '$');

            hashTable->Insert(bid);
            bidCount++;
        }

        cout << bidCount << " bids read" << endl;

    }
    catch (csv::Error& e) {
        std::cerr << e.what() << std::endl;
    }
}

// Convert string to double
double strToDouble(string str, char ch) {
    str.erase(remove(str.begin(), str.end(), ch), str.end());
    return atof(str.c_str());
}

// Main
int main(int argc, char* argv[]) {
    string csvPath, bidKey;
    switch (argc) {
    case 2:
        csvPath = argv[1];
        bidKey = "98223";
        break;
    case 3:
        csvPath = argv[1];
        bidKey = argv[2];
        break;
    default:
        csvPath = "eBid_Monthly_Sales.csv";
        bidKey = "98223";
    }

    clock_t ticks;
    HashTable* bidTable = new HashTable();
    Bid bid;
    int choice = 0;

    while (choice != 9) {
        cout << "Menu:" << endl;
        cout << "  1. Load Bids" << endl;
        cout << "  2. Display All Bids" << endl;
        cout << "  3. Find Bid" << endl;
        cout << "  4. Remove Bid" << endl;
        cout << "  9. Exit" << endl;
        cout << "Enter choice: ";
        cin >> choice;

        switch (choice) {
        case 1:
            ticks = clock();
            loadBids(csvPath, bidTable);
            ticks = clock() - ticks;
            cout << "time: " << ticks << " clock ticks" << endl;
            cout << "time: " << ticks * 1.0 / CLOCKS_PER_SEC << " seconds" << endl;
            break;
        case 2:
            bidTable->PrintAll();
            break;
        case 3: {
            // ask the user for the bid id to find
            std::string inputKey;
            cout << "Enter Bid Id to find: ";
            cin >> inputKey;

            ticks = clock();
            bid = bidTable->Search(inputKey);
            ticks = clock() - ticks;

            if (!bid.bidId.empty()) {
                displayBid(bid);
            } else {
                cout << "Bid Id " << inputKey << " not found." << endl;
            }
            cout << "time: " << ticks << " clock ticks" << endl;
            cout << "time: " << ticks * 1.0 / CLOCKS_PER_SEC << " seconds" << endl;
            break;
        }
        case 4: {
            // ask the user for the bid id to remove
            std::string inputKey;
            cout << "Enter Bid Id to remove: ";
            cin >> inputKey;
            bidTable->Remove(inputKey);
            break;
        }
        }
    }

    cout << "Good bye." << endl;
    return 0;
}