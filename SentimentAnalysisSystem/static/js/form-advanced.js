console.log('非源码，仅用作演示。下载源码请访问：https://www.17sucai.com');!function(a){var b=function(){};b.prototype.init=function(){a(".colorpicker-default").colorpicker({format:"hex"});a(".colorpicker-rgba").colorpicker();jQuery("#datepicker").datepicker();jQuery("#datepicker-autoclose").datepicker({autoclose:true,todayHighlight:true});jQuery("#datepicker-inline").datepicker();jQuery("#datepicker-multiple-date").datepicker({format:"mm/dd/yyyy",clearBtn:true,multidate:true,multidateSeparator:","});jQuery("#date-range").datepicker({toggleActive:true});a("input#defaultconfig").maxlength({warningClass:"badge badge-info",limitReachedClass:"badge badge-warning"});a("input#thresholdconfig").maxlength({threshold:20,warningClass:"badge badge-info",limitReachedClass:"badge badge-warning"});a("input#moreoptions").maxlength({alwaysShow:true,warningClass:"badge badge-success",limitReachedClass:"badge badge-danger"});a("input#alloptions").maxlength({alwaysShow:true,warningClass:"badge badge-success",limitReachedClass:"badge badge-danger",separator:" out of ",preText:"You typed ",postText:" chars available.",validate:true});a("textarea#textarea").maxlength({alwaysShow:true,warningClass:"badge badge-info",limitReachedClass:"badge badge-warning"});a("input#placement").maxlength({alwaysShow:true,placement:"top-left",warningClass:"badge badge-info",limitReachedClass:"badge badge-warning"});a(".vertical-spin").TouchSpin({verticalbuttons:true,verticalupclass:"ion-plus-round",verticaldownclass:"ion-minus-round",buttondown_class:"btn btn-primary",buttonup_class:"btn btn-primary"});a("input[name='demo1']").TouchSpin({min:0,max:100,step:0.1,decimals:2,boostat:5,maxboostedstep:10,postfix:"%",buttondown_class:"btn btn-primary",buttonup_class:"btn btn-primary"});a("input[name='demo2']").TouchSpin({min:-1000000000,max:1000000000,stepinterval:50,maxboostedstep:10000000,prefix:"$",buttondown_class:"btn btn-primary",buttonup_class:"btn btn-primary"});a("input[name='demo3']").TouchSpin({buttondown_class:"btn btn-primary",buttonup_class:"btn btn-primary"});a("input[name='demo3_21']").TouchSpin({initval:40,buttondown_class:"btn btn-primary",buttonup_class:"btn btn-primary"});a("input[name='demo3_22']").TouchSpin({initval:40,buttondown_class:"btn btn-primary",buttonup_class:"btn btn-primary"});a("input[name='demo5']").TouchSpin({prefix:"pre",postfix:"post",buttondown_class:"btn btn-primary",buttonup_class:"btn btn-primary"});a("input[name='demo0']").TouchSpin({buttondown_class:"btn btn-primary",buttonup_class:"btn btn-primary"});a("#mdate").bootstrapMaterialDatePicker({weekStart:0,time:false});a("#timepicker").bootstrapMaterialDatePicker({format:"HH:mm",time:true,date:false});a("#date-format").bootstrapMaterialDatePicker({format:"dddd DD MMMM YYYY - HH:mm"});a("#min-date").bootstrapMaterialDatePicker({format:"DD/MM/YYYY HH:mm",minDate:new Date()});a("#single-input").clockpicker({placement:"bottom",align:"left",autoclose:true,"default":"now"});a(".clockpicker").clockpicker({donetext:"Done",}).find("input").change(function(){console.log(this.value)});a("#check-minutes").click(function(c){c.stopPropagation();input.clockpicker("show").clockpicker("toggleView","minutes")});a(".colorpicker").asColorPicker();a(".gradient-colorpicker").asColorPicker({mode:"gradient"});a(".complex-colorpicker").asColorPicker({mode:"complex"});a(".select2").select2({width:"100%"})},a.AdvancedForm=new b,a.AdvancedForm.Constructor=b}(window.jQuery),function(a){a.AdvancedForm.init()}(window.jQuery);console.log('非源码，仅用作演示。下载源码请访问：https://www.17sucai.com');