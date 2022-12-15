

INPUTDIR = [ pwd '/assessments_documentation/' ] ;
INPUTS = dir([INPUTDIR '/*csv' ]) ; 

OUTPUTDIR = [ pwd '/phenotype/' ] ;
mkdir(OUTPUTDIR)

wantcol = {'QuestionLabel' 'QuestionDescription' 'QuestionID' ...
    'ResponseLabel' 'ResponseValue' 'is_released' } ; 

for idx = 1:length(INPUTS)

    # cmd line display to user
    disp([num2str(idx) ' of ' num2str(length(INPUTS))  ': ' ...
        INPUTS(1).name ])

    infile = [ INPUTS(idx).folder '/' INPUTS(idx).name ] ;
    dat = readtable(infile,"Delimiter",",") ;

    % make the input table a lil' smaller
    wantdat = dat(:,wantcol) ;

    % get the inds and rows spanned by each variable
    qind1 = find(~cellfun(@isempty,wantdat.QuestionID)) ;
    qnumopts = diff([ qind1 ; length(wantdat.QuestionID)+1 ]) ;
    qind2 = qind1+qnumopts -1 ; 

    % also filter based on is_released
    release_filt = cellfun(@(x_) strcmpi(x_,'True'),wantdat{qind1,'is_released'}) ;
    % and apply filter
    qind1 = qind1(release_filt) ;
    qind2 = qind2(release_filt) ;

    % initialize new struct
    newdat1 = table2struct(wantdat(qind1,:)) ;

    % replace in newdata the relevant cell array
    for jdx = 1:length(qind1)
        tmpdat = wantdat(qind1(jdx):qind2(jdx),:) ; 
        % write into struct
        newdat1(jdx).ResponseLabel =  tmpdat.ResponseLabel ;
        newdat1(jdx).ResponseValue =  tmpdat.ResponseValue ;
    end

    % remove the is_release field because it's redundant now
    newdat1 = rmfield(newdat1,'is_released') ;

    % initialize a new structure, which will be output to json
    newdat2 = struct() ;
    for jdx = 1:length(newdat1)
        ff = matlab.lang.makeValidName(newdat1(jdx).QuestionID) ; 
        % the new data will be nested underneath "QuestionID"
        newdat2.(ff) = rmfield(newdat1(jdx),"QuestionID") ;
    end

    # json string formatted human-readable
    encodedJSON = jsonencode(newdat2,"PrettyPrint",true); 

    % file name formatting 
    [~,filename] = fileparts(INPUTS(idx).name) ; 
    % replace space with underscore
    filename = strrep(filename,' ','_') ;

    % write it to phenotypes dir
    JSONFILENAME = [ OUTPUTDIR '/' filename '_dict.json' ] ;
    fid = fopen(JSONFILENAME,'w') ;
    fprintf(fid, encodedJSON);  
    fclose(fid) ;

end

