#include <iostream>
#include <string>

unsigned int lose_num;
unsigned int max_count;
bool first_count;
unsigned int cur_num;
unsigned int target_num;


void setgame(){
    while(true){
        std::cout << "먼저 말하면 패배하는 숫자를 정하세요(31 대신 쓸 숫자): ";
        try{
            std::cin >> lose_num;
            std::cout << "먼저 말하면 패배하는 숫자: " << lose_num << std::endl;
            if (lose_num < 9){
                std::cout << std::endl << "숫자가 너무 작습니다!" << std::endl;
                continue;
            }
            if (lose_num >500){
                std::cout << std::endl << "숫자가 너무 큽니다!(500 이하)" << std::endl;
            }
        }
        catch(...){
            std::cout << std::endl << "오류" << std::endl;
            continue;
        }
        break;
    }

    while(true){
        std::cout << "말할 수 있는 숫자 최대값을 정하세요: ";
        try{
            std::cin >> max_count;
            std::cout << "최대 " << max_count << "개 숫자를 말할 수 있습니다" << std::endl;
            if (max_count*4 > lose_num){
                std::cout << std::endl << "숫자가 너무 큽니다!" << std::endl;
                continue;
            }
            if (max_count < 2){
                std::cout << std::endl << "숫자가 너무 작습니다!" << std::endl;
                continue;
            }
        }
        catch(...){
            std::cout << std::endl << "오류" << std::endl;
            continue;
        }
        break;   
    }

    while(true){
        std::string str;
        std::cout << "먼저 하시겠습니까? (y/n)";
        try{
            std::cin >> str;
            if (str != "Y" and str != "y" and str != "N" and str != "n" ){
                std::cout << std::endl << "type y for yes, n for no" << std::endl;
                continue;
            }
            if (str == "Y" or str == "y"){
                first_count = true;
            }
            else{
                first_count = false;
            }
        }
        catch(...){
            std::cout << std::endl << "오류" << std::endl;
            continue;
        }
        std::cout << std::endl;
        break;
    }
    
}

int getline(std::string str){
    std::string numstr = "";
    unsigned int strnum;
    unsigned int curstrnum; curstrnum = cur_num;
    unsigned int cur_count = 0;

    for (char s : str){
        if (s == ' '){
            if (numstr == ""){
                continue;
            }
            strnum = stoi(numstr);
            if (strnum != curstrnum){  
                std::cout << "숫자를 순서대로 쓰세요!!" << std::endl;
                return 1;
            };
            ++cur_count;
            ++curstrnum;
            if (cur_count > max_count){
                std::cout << "숫자를 최대 " << max_count << "개까지만 쓰세요!!" << std::endl;
                return 1;
            }
            numstr = "";
        }
        else{
            numstr += s;
        }
    }
    if (numstr != ""){
        strnum = stoi(numstr);
        if (strnum != curstrnum){  
            std::cout << "숫자를 순서대로 쓰세요!!" << std::endl;
            return 1;
        };
        ++cur_count;
        ++curstrnum;
        if (cur_count > max_count){
            std::cout << "숫자를 최대 " << max_count << "개까지만 쓰세요!!" << std::endl;
            return 1;
        }
    }
    if (cur_count == 0){
        std::cout << "숫자를 하나 이상 쓰세요!!" << std::endl;
        return 1;
    }
    cur_num += cur_count;
    return 0;
}

void userturn(){
    std::cout << "유저차례" << std::endl;
    while (true){
        std::string str = "";
        std::cout << "숫자를 입력하세요: ";
        try {
            std::getline(std::cin >> std::ws, str);
        }
        catch(...){
            std::cout << "Error!" << std::endl;
            continue;
        }
        if (getline(str) == 0) break;
    }
    if (target_num < cur_num) target_num += max_count + 1;
}

void opturn(){
    std::cout << "\n컴퓨터 차례" << std::endl;
    if (target_num >= cur_num + max_count){
        std::cout << cur_num++ << std::endl;
    }
    else {
        for (; cur_num<=target_num;){
            std::cout << cur_num++ << " ";
        }
        std::cout << std::endl;
    }
    std::cout << "숫자를 원하는 만큼 말했습니다\n" << std::endl;
}

int main(){
    system("chcp 65001");
    std::cout << "베스킨라빈스 게임!!!!!!" << std::endl;
    std::cout << "두명이 번갈아서 차례대로 숫자를 말합니다" << std::endl;
    std::cout << "숫자는 세개까지 말할 수 있습니다" << std::endl;
    std::cout << "31을 먼저 말하는 사람이 패배!!" << std::endl;
    while (true){
        setgame();
        target_num = (lose_num-1)-(max_count+1)*((lose_num-1)/(max_count+1));
        cur_num = 1;
        if (target_num==0) target_num += max_count +1;

        if (first_count){
            std::cout << "숫자를 원하는 만큼 1부터 차례로 입력하세요" << std::endl;
            std::cout << "예시: \n1 2 3" << std::endl;
            userturn();
        }

        while (true){
            opturn();
            if(cur_num == lose_num){
                std::cout << "You lose" << std::endl;
                break;
            }

            userturn();
            if(cur_num == lose_num){
                std::cout << "You win!!!" << std::endl;
                break;
            }
        }
        std::cout << "다시 하시려면 아무거나 입력하고 Enter를 누르세요\n 끝내려면 Ctrl+C를 누르세요" << std::endl;
        std::string l;
        std::cin >> l;
        std::cout << std::endl;
    }
}
