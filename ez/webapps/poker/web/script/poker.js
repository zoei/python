// 种类
kinds = ["单牌", "双对", "三对", "三带一", "三带二", "单顺", "双顺", "三顺", "四顺", "三顺带单", "三顺带双", "四顺带二单", "四顺带二对", "炸弹", "火箭"];
// 最小数量，等于
count_min = [1, 2, 3, 4, 5, 5, 6, 6, 8, 8, 10, 6, 8, 4, 2];
// 最大数量，不等于
count_max = [2, 3, 4, 5, 6, 13, 21, 19, 21, 17, 16, 19, 17, 5, 3];
// 步长值
count_step = [1, 1, 1, 1, 1, 1, 2, 3, 4, 4, 5, 6, 8, 1, 1];
// 每种牌的最大值
value_max = [13, 12, 12, 12, 12, 11, 11, 11, 11, 11, 11, 12, 12, 12];
function Card(index){
	this.index = index;
	this.value = parseInt(index / 4);
	this.html = "<img id='" + index + "' src='images/" + index + ".png'>";
}
function Cards(indexs){
	this.kind = -1;
	this.value = -1;
	if(indexs == undefined){
		this.indexs = new Array();
		for(var i=0;i<54;i++){
			this.indexs.push(i);
		}
	}else if(indexs.length == 0){
		this.indexs = new Array();
	}else{
		this.indexs = indexs;
	}
	this.cards = new Array();
	this.values = new Array();
	for(var i in this.indexs){
		var index = this.indexs[i];
		var card = new Card(index);
		this.values.push(parseInt(index / 4));
		this.cards.push(card);
	}
	this.shuffle = function(){
	    var tmp_indexs = this.indexs;
	    var tmp_cards = this.cards;
	    var tmp_random = new Array();
	    this.indexs = new Array();
	    this.values = new Array();
	    this.cards = new Array();
	    while(tmp_random.length < tmp_indexs.length){
	    	var r = parseInt(Math.floor(Math.random() * tmp_indexs.length));
	    	if(indexOf(r, tmp_random) == -1){
	    		tmp_random.push(r);
	    		this.indexs.push(tmp_indexs[r]);
	    		this.values.push(parseInt(tmp_indexs[r] / 4));
	    		this.cards.push(tmp_cards[r]);
	    	}
	    }
	    tmp_indexs = undefined;
	    tmp_cards = undefined;
	    tmp_random = undefined;
	    return this;
	};

	this.sort = function(){
	    this.cards = new Array();
	    this.indexs.sort(sortNumber);
	    this.values.sort(sortNumber);
	    for(var i in this.indexs){
	    	this.cards.push(new Card(this.indexs[i]));
	    }
	    return this;
	};

	this.append = function(cards){
		this.cards = this.cards.concat(cards.cards);
	    for(var i in cards.indexs){
	    	this.indexs.push(cards.indexs[i]);
	        this.values.push(parseInt(cards.indexs[i]/4));
	    }
	    return this;
	};

	this.remove = function(cards){
		for(var i in cards.indexs){
			var index = indexOf(cards.indexs[i], this.indexs);
			if( index != -1){
				this.cards.splice(index,1);
		    	this.indexs.splice(index,1);
		        this.values.splice(index,1);
			}
		}
	    return this;
	};
	
	this.size = function(){
	    return this.indexs.length;
	};
	
// ===================================================================
    this.compare = function(compare_to_cards){
        if (this.kind == -1){
            return -99;
        }
        var kind_come = compare_to_cards.kind;
        var value_come = compare_to_cards.value;
        if (this.kind == kind_come){
            if (this.size() == compare_to_cards.size()){
                if (this.value == 13 && value_come == 13){
                    return cmp(this.indexs[0], compare_to_cards.indexs[0]);
                }else{
                    return cmp(this.value, value_come);
                }
            }else{
                return -99;
            }
        }else{
            if (this.kind < 12 && kind_come < 12){
                return -99;
            }else{
                return cmp(this.kind, kind_come);
            }
        }
    };

    this.get_kind_value = function(){
        var count = this.sort().size();
        for(var i=0;i<kinds.length;i++){
            if (inRange(count, count_min[i], count_max[i], count_step[i])){
                var kind_value = eval("this.is_kind"+i+"()");
                this.kind = kind_value[0];
                this.vlaue = kind_value[1];
                alert(kinds[this.kind]);
                if(this.kind != -1){
                    break;
                }
            }
        }
        return [this.kind, this.value];
    };

// 返回顺子的最大值
    this.is_order = function(values){
        var value = values[0];
        if (values.length == 1){
            return value;
        }
        tmp_values = values.slice(1);
        for(var i in tmp_values){
            if (tmp_values[i] - value != 1){
                return -1;
            }
            value = tmp_values[i];
        }
        return value;
    };
// 单牌
    this.is_kind0 = function(){
        return [0, this.values[0]];
    };
// 双对
    this.is_kind1 = function(){
        var value = this.get_same_value(this.values);
        if (value == -1){
            return [-1, -1];
        }else if (value == 13){
            return [13, 13];
        }else{
            return [1, value];
        }
    };
// 三对
    this.is_kind2 = function(){
        var value = this.get_same_value(this.values);
        if (value == -1){
            return [-1, -1];
        }else{
            return [2, value];
        }
    };
// 三带一
    this.is_kind3 = function(){
        for(var i in this.values){
            if(this.count(this.values[i]) == 3){
                return [3, this.values[i]];
            }
        }
        return [-1, -1];
    };
// 三带二
    this.is_kind4 = function(){
        if (this.get_same_value(this.values.slice(0,2)) != -1 &&
                this.get_same_value(this.values.slice(2)) != -1){
            return [4, this.values[-1]];
        }
        if (this.get_same_value(this.values.slice(0,3)) != -1 &&
                this.get_same_value(this.values.slice(3)) != -1){
            return [4, this.values[0]];
        }
        return [-1, -1];
    };
// 单顺
    this.is_kind5 = function(){
        var value = this.is_order(this.values);
        if (value != -1 && value <= value_max[5]){
            return [5, value];
        }else{
            return[-1, -1];
        }
    };
// 双顺
    this.is_kind6 = function(){
        var size = this.values.length;
        var value = this.values[0];
        if (value != this.values[1]){
            return [-1, -1];
        }
        for(var i=2;i<size;i+=2){
            if (this.values[i] != this.values[i + 1] || (this.values[i] - value) != 1 || this.values[i] > value_max[6]){
                return [-1, -1];
            }
            value = this.values[i];
        }
        return [6, this.values[-1]];
    };
// 三顺
    this.is_kind7 = function(){
        var size = this.values.length;
        var value = this.values[0];
        if(value != this.values[1] || value != this.values[2]){
            return [-1, -1];
        }
        for(var i=3;i<size;i+=3){
            if (this.values[i] != this.values[i + 1] || this.values[i] != this.values[i + 2]
                    || (this.values[i] - value) != 1 || this.values[i] > value_max[7]){
                return [-1, -1];
            }
            value = this.values[i];
        }
        return [7, this.values[size-1]];
    };
// 四顺
    this.is_kind8 = function(){
        var size = this.values.length;
        var tmp_values = new Array();
        var i = 0;
        while(i < size){
            var count = this.count(this.values[i]);
            if (this.values[i] > value_max[8] || count != 4){
                return[-1, -1];
            }
            tmp_values.push(this.values[i]);
            i += count;
        }
        var value = this.is_order(tmp_values);
        if (value != -1){
            tmp_values = undefined;
            return[8, value];
        }
        return [-1, -1];
    };
// 三顺带单
    this.is_kind9 = function(){
        var size = this.values.length;
        var tmp_values = new Array();
        var i = 0;
        while(i < size){
            var count = this.count(this.values[i]);
            if (this.values[i] <= value_max[9] && count >= 3){
                tmp_values.push(this.values[i]);
            }
            i += count;
        }
        if (tmp_values.length > parseInt(size / count_step[9])){
            var value = this.is_order(tmp_values.slice(1));
            if (value != -1){
                tmp_values = undefined;
                return[9, value];
            }
            value = this.is_order(tmp_values.slice(0,tmp_values.length-1));
            if (value != -1){
                tmp_values = undefined;
                return[9, value];
            }
        }else if (tmp_values.length == parseInt(size / count_step[9])){
            value = this.is_order(tmp_values);
            if (value != -1){
                tmp_values = undefined;
                return[9, value];
            }
        }
        return [-1, -1];
    };
// 三顺带双
    this.is_kind10 = function(){
        var size = this.values.length;
        var tmp_values = new Array();
        var i = 0;
        while(i < size){
            count = this.count(this.values[i]);
            if (this.values[i] <= value_max[10] && count == 3){
                tmp_values.push(this.values[i]);
            }else if (count % 2 != 0){
                return[-1, -1];
            }
            i += count;
        }

        if (tmp_values.length == parseInt(size / 5)){
            var value = this.is_order(tmp_values);
            if (value != -1){
                tmp_values = undefined;
                return[10, value];
            }
        }
        return [-1, -1];
    };
// 四顺带二单
    this.is_kind11 = function(){
        var size = this.values.length;
        var tmp_values = new Array();
        var i = 0;
        while(i < size){
            count = this.count(this.values[i]);
            if (this.values[i] <= value_max[11] && count == 4){
                tmp_values.push(this.values[i]);
            }
            i += count;
        }
        if (tmp_values.length > parseInt(size / count_step[11])){
            var value = this.is_order(tmp_values.slice(1));
            if (value != -1){
                tmp_values = undefined;
                return[11, value];
            }
            value = this.is_order(tmp_values.slice(0,tmp_values.length-1));
            if (value != -1){
                tmp_values = undefined;
                return[11, value];
            }
        }
        else if (tmp_values.length == parseInt(size / count_step[11])){
            value = this.is_order(tmp_values);
            if (value != -1){
                tmp_values = undefined;
                return[11, value];
            }
        }
        return [-1, -1];
    };
// 四顺带二对
    this.is_kind12 = function(){
    	alert("四顺带二对test");
        var size = this.values.length;
        var tmp_values = new Array();
        var i = size - 1;
        while(i >= 0){
            var count = this.count(this.values[i]);
            if (this.values[i] <= value_max[12] && count == 4){
                tmp_values.push(this.values[i]);
            }else if (count % 2 != 0){
                return[-1, -1];
            }
            i -= count;
        }
        if (tmp_values.length == parseInt(size / count_step[12])){
            value = this.is_order(tmp_values);
            if (value != -1){
                tmp_values = undefined;
                return[12, value];
            }
        }else if (len(tmp_values) > size / count_step[12]){
            value = tmp_values[0];
            for( i in tmp_values.slice(1)){
                if (value - i == 1){
                    return (12, value);
                }
                value = i;
            }
        }
        return [-1, -1];
    };  
// 炸弹
    this.is_kind13 = function(){
        var value = this.get_same_value(this.values);
        if (value == -1){
            return [-1, -1];
        }else{
            return [13, value];
        }
    };
// 火箭
    this.is_kind14 = function(){
        var value = this.get_same_value(this.values);
        if (value == -1){
            return [-1, -1];
        }else if(value == 13){
            return (14, 13);    
        }else{
            return [1, value];
        }
    };
// 取得相同的值
    this.get_same_value = function(values){
        if (values[0] != values[values.length-1]){
            return -1;
        }else{
            return values[0];
        }
	};
// 取得某个元素的个数
	this.count = function(element){
		var n = 0;
		for(var i in this.values){
			if(this.values[i] == element){
				n++;
			}
		}
		return n;
	};
}

function indexOf(value, array){
	for(var i in array){
		if(value == array[i]){
			return i;
		};
	}
	return -1;
}

function cardIndexOf(value, array){
	for(var i in array){
		if(value.index == array[i].index){
			return i;
		};
	}
	return -1;
}

function sortNumber(a, b){
	return a - b;
}

function range(start, end, step){
	var array = new Array();
	for(var i=start;i<end;i+=step){
		array.push(i);
	}
	return array;
}
function inRange(n, start, end, step){
	for(var i=start;i<end;i+=step){
		if(n == i){
			return true;
		}
	}
	return false;
}

function cmp(a, b){
	if(a - b ==0){
		return 0;
	}else{
		return (a-b)/Math.abs(a-b);
	}
}


