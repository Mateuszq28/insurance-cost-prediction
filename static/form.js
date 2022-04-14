$('#sendAnswers_button').click(function (event) {
    // Sprawdzenie, czy wszystkie obowiązkowe pola są wypełnione
    var allAreFilled = true;
    document.getElementById('myForm').querySelectorAll('[required]').forEach(function (i) {
        if (!allAreFilled) return;
        if (!i.value) allAreFilled = false;
        if (i.type === 'radio') {
            let radioValueCheck = false;
            document.getElementById('myForm').querySelectorAll(`[name=${i.name}]`).forEach(function (r) {
                if (r.checked) radioValueCheck = true;
            });
            allAreFilled = radioValueCheck;
        }
    });
    if (!allAreFilled) {
        alert('Wypełnij wszystkie pola formularza!');
    } else {
        // pobieranie odpowiedzi z kolejnych pytań

        var qanswers = new Array(9);
        var qname_arr = ['fname', 'height', 'lname', 'weight', 'today_date', 'kids', 'sex', 'smoking', 'age', 'race'];
        for (var j = 0; j < 10; j++) {
            var qname = qname_arr[j];
            var radios_q = document.getElementsByName(qname);

            if (qname == 'sex' || qname == 'smoking') {
                for (var i = 0, length = radios_q.length; i < length; i++) {
                    if (radios_q[i].checked) {
                        // pobranie wartości przypisanej do zaznaczonego radiobutton'a
                        qanswers[j] = radios_q[i].value;
                        break;
                    }
                }
            }
        }

        var height = document.getElementsByName('height')[0].value;
        var weight = document.getElementsByName('weight')[0].value;
        var today_date = document.getElementsByName('today_date')[0].value;
        var kids = document.getElementsByName('kids')[0].value;
        var sex = qanswers[6];
        var smoking = qanswers[7];
        var age = document.getElementsByName('age')[0].value;
        var race = document.getElementsByName('race')[0].value;
        var expenses = document.getElementsByName('expenses')[0].value;

        //console.log(height);
        //console.log(weight);
        //console.log(today_date);
        //console.log(kids);
        //console.log(sex);
        //console.log(smoking);
        //console.log(age);
        //console.log(race);

        // utworzenie obiektu JSON
        const message = {
            height: height,
            weight: weight,
            today_date: today_date,
            kids: kids,
            sex: sex,
            smoking: smoking,
            age: age,
            race: race,
            expenses: expenses
        };
        const message_stringify = JSON.stringify(message);
        document.getElementById('survey_result').innerHTML = "Obliczanie..."

        // przesyłanie obiektu JSON metodą post
        $.post('http://127.0.0.1:5000/calculate', message_stringify, function (response) {
            //response - odpowiedź zwrotna w formacie JSON przesyłana przez serwer
            //console.log("odebrano");
            var response_info = response['info'];
            var response_dolar = response['expenses_d'];
            var response_pln = response['expenses_pln'];
            var response_dolar_price = response['dolar_price'];
            //console.log("odebrano_poprawnie");

            print_result = 'Twoje ubezpieczenie będzie kosztowało ' + response_dolar + ' dolarów,<br>';
            print_result += 'co przy kursie ' + response_dolar_price + ' będzie wynosiło ' + response_pln + ' zł.';
            document.getElementById('survey_result').innerHTML = print_result
        });
    }
});
